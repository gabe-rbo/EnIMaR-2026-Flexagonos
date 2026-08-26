"""
Módulo de Coloração de Domínio (Domain Coloring) para Funções Complexas.
Desenvolvido para o projeto EnIMaR 2026 (Flexágonos e Funções Complexas).

Suporta:
- Retratos de fase contínuos (HSV clássico e com ênfase em módulo/argumento)
- Reticulados aprimorados no estilo Elias Wegert (linhas de nível do módulo e raios de fase)
- Coloração por Cores Sólidas (discretização angular em N setores e xadrez polar)
- Mapeamento Conforme de Textura / Imagem Arbitrária no plano w (Image Pullback: f*(I))
- Geradores paramétricos de padrões no plano w (grade cartesiana, xadrez, Truchet, alvos)
- Geração de faces de flexágonos em alta resolução (compatível com Facas e Planificações)
"""

from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple, Union
import numpy as np
from PIL import Image
import cv2


# ==============================================================================
# PALETAS DE CORES SÓLIDAS PADRÃO
# ==============================================================================

# Paleta padrão de 6 cores puras (para 6 faces de flexágono ou 6 setores de 60 graus)
PALETTE_SOLID_6 = np.array([
    [230,  25,  25],  # 0: Vermelho  [0°, 60°)
    [245, 185,   0],  # 1: Amarelo   [60°, 120°)
    [ 25, 175,  45],  # 2: Verde     [120°, 180°)
    [  0, 200, 230],  # 3: Ciano     [180°, 240°)
    [ 30,  70, 225],  # 4: Azul      [240°, 300°)
    [210,  30, 210],  # 5: Magenta   [300°, 360°)
], dtype=np.uint8)

# Paleta padrão de 12 cores sólidas (setores de 30 graus)
PALETTE_SOLID_12 = np.array([
    [240,  30,  30],  # 0°   Vermelho
    [245, 120,   0],  # 30°  Laranja
    [245, 200,   0],  # 60°  Amarelo
    [160, 220,  20],  # 90°  Lima
    [ 30, 185,  45],  # 120° Verde
    [ 20, 200, 140],  # 150° Verde-Água
    [  0, 205, 235],  # 180° Ciano
    [ 20, 130, 240],  # 210° Azul Celeste
    [ 35,  70, 225],  # 240° Azul Real
    [130,  40, 220],  # 270° Roxo
    [210,  30, 210],  # 300° Magenta
    [235,  25, 130],  # 330° Rosa/Carmim
], dtype=np.uint8)

# Paleta de 4 cores sólidas (quadrantes)
PALETTE_SOLID_4 = np.array([
    [230,  40,  40],  # Q1 (0° a 90°): Vermelho
    [ 40, 180,  60],  # Q2 (90° a 180°): Verde
    [  0, 160, 235],  # Q3 (180° a 270°): Ciano/Azul
    [220, 170,  20],  # Q4 (270° a 360°): Amarelo/Dourado
], dtype=np.uint8)


# ==============================================================================
# AVALIAÇÃO DE MALHA COMPLEXA
# ==============================================================================

def evaluate_complex_grid(
    func: Callable[[np.ndarray], np.ndarray],
    x_range: Tuple[float, float] = (-2.0, 2.0),
    y_range: Tuple[float, float] = (-2.0, 2.0),
    width: int = 1000,
    height: int = 1000
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Avalia a função complexa f(z) sobre uma malha retangular no plano complexo.

    Retorna:
        Z: malha de pontos complexos z = x + iy (shape: height, width)
        W: valores calculados w = f(z) com NaNs/Infs tratados
    """
    x = np.linspace(x_range[0], x_range[1], width, dtype=np.float64)
    # y_range[1] em cima (linha 0) até y_range[0] embaixo (linha height-1)
    y = np.linspace(y_range[1], y_range[0], height, dtype=np.float64)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
        try:
            W = func(Z)
        except Exception:
            # Fallback caso a função não seja vetorizada nativamente
            vf = np.vectorize(func)
            W = vf(Z)

    # Substituir valores indefinidos por zero ou magnitudes seguras
    W = np.nan_to_num(W, nan=0.0, posinf=1e10, neginf=-1e10)
    return Z, W


# ==============================================================================
# MODOS DE COLORAÇÃO
# ==============================================================================

def colorize_continuous_hsv(
    w: np.ndarray,
    hue_shift: float = 0.0,
    saturation: float = 1.0,
    brightness_mode: str = 'constant',
    min_brightness: float = 0.2,
    max_brightness: float = 1.0,
    gamma: float = 1.0
) -> np.ndarray:
    """
    Coloração de domínio contínua padrão usando espaço de cor HSV.

    Parâmetros:
        w: array complexo w = f(z)
        hue_shift: deslocamento angular do matiz [0, 1] (ex: 0.5 rotaciona 180°)
        saturation: saturação [0, 1]
        brightness_mode: 'constant', 'log_modulus', 'smooth_phase' ou 'balanced'
        min_brightness, max_brightness: limites de valor/brilho
        gamma: expoente de correção de brilho
    """
    # Ângulo normalizado no intervalo [0, 1)
    arg = np.angle(w)
    arg = np.where(arg < 0, arg + 2 * np.pi, arg)
    hue = (arg / (2 * np.pi) + hue_shift) % 1.0

    H_tex = hue * 179.0  # OpenCV usa H em [0, 179]
    S_tex = np.full_like(hue, saturation * 255.0)

    if brightness_mode == 'constant':
        V_tex = np.full_like(hue, max_brightness * 255.0)

    elif brightness_mode == 'log_modulus':
        modulus = np.abs(w)
        log_mod = np.log(modulus + 1e-10)
        l_min, l_max = log_mod.min(), log_mod.max()
        if l_max > l_min:
            norm_mod = (log_mod - l_min) / (l_max - l_min)
        else:
            norm_mod = np.zeros_like(log_mod)
        norm_mod = norm_mod ** gamma
        val = min_brightness + (max_brightness - min_brightness) * norm_mod
        V_tex = np.clip(val * 255.0, 0, 255)

    elif brightness_mode == 'balanced':
        # Efeito suave de luz: realça zeros (escuros) e polos (claros)
        modulus = np.abs(w)
        # Transformação sigmoidal suave centrada em |w| = 1
        val = 1.0 - 1.0 / (1.0 + modulus ** 0.5)
        val = min_brightness + (max_brightness - min_brightness) * (val ** gamma)
        V_tex = np.clip(val * 255.0, 0, 255)

    else:
        V_tex = np.full_like(hue, 255.0)

    hsv = np.stack([H_tex, S_tex, V_tex], axis=-1).astype(np.uint8)
    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    return rgb


def colorize_wegert_enhanced(
    w: np.ndarray,
    n_mod_lines: int = 10,
    n_phase_lines: int = 12,
    hue_shift: float = 0.0,
    pattern_mode: str = 'both',
    contrast: float = 0.6,
    min_brightness: float = 0.35,
    max_brightness: float = 0.95,
    **kwargs
) -> np.ndarray:
    """
    Coloração aprimorada no estilo de Elias Wegert (Enhanced Phase Plots),
    adicionando linhas de nível isomodulares e isocromáticas por função dente-de-serra (sawtooth).

    Modos de padrão (pattern_mode) suportados:
        'modulus': apenas curvas de nível de módulo |f(z)|
        'phase': apenas raios de argumento arg(f(z))
        'both': linhas de módulo e fase multiplicadas (polar grid)
        'polar_tiles': ladrilhamento polar com fase discretizada
    """
    pattern_mode = kwargs.get('mode', pattern_mode)
    arg = np.angle(w)
    arg = np.where(arg < 0, arg + 2 * np.pi, arg)
    arg_norm = arg / (2 * np.pi)

    if pattern_mode == 'polar_tiles':
        # Discretizar o matiz para cada setor
        phase_discrete = np.floor(arg_norm * n_phase_lines) / n_phase_lines
        hue = (phase_discrete + hue_shift) % 1.0
    else:
        hue = (arg_norm + hue_shift) % 1.0

    # Sawtooth para o módulo (anéis concêntricos no plano w)
    modulus = np.abs(w)
    log_mod = np.log(modulus + 1e-10)
    # Normalização estável para o módulo
    scaled_mod = n_mod_lines * (log_mod / (2 * np.pi))
    sawtooth_mod = np.ceil(scaled_mod) - scaled_mod

    # Sawtooth para a fase (raios isocromáticos)
    x_phase = n_phase_lines * arg_norm
    sawtooth_phase = np.ceil(x_phase) - x_phase

    if pattern_mode == 'modulus':
        sawtooth = sawtooth_mod
    elif pattern_mode == 'phase':
        sawtooth = sawtooth_phase
    else:  # 'both' ou 'polar_tiles'
        sawtooth = sawtooth_mod * sawtooth_phase

    # Compressão não-linear de contraste
    sawtooth_compressed = np.clip(sawtooth, 0.0, 1.0) ** contrast
    value = min_brightness + (max_brightness - min_brightness) * sawtooth_compressed
    value = np.clip(value, min_brightness, max_brightness)

    H_tex = (hue * 179.0).astype(np.uint8)
    S_tex = np.full_like(H_tex, 255)
    V_tex = (value * 255.0).astype(np.uint8)

    hsv = np.stack([H_tex, S_tex, V_tex], axis=-1)
    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    return rgb


def colorize_solid_sectors(
    w: np.ndarray,
    n_sectors: int = 6,
    palette: Optional[np.ndarray] = None,
    hue_shift: float = 0.0,
    mark_zeros_poles: bool = False,
    zero_threshold: float = 0.02,
    pole_threshold: float = 50.0
) -> np.ndarray:
    """
    Coloração de domínio em Cores Sólidas (*Solid Colors*).
    Discretiza o plano w em N setores angulares de cores puras e planas, sem gradientes.

    Parâmetros:
        w: array complexo
        n_sectors: número de setores angulares (padrão: 6)
        palette: array uint8 de shape (N, 3) com as cores RGB de cada setor
        hue_shift: rotação angular das paletas [0, 1]
        mark_zeros_poles: se True, colore zeros em preto e polos em branco
    """
    if palette is None:
        if n_sectors == 6:
            palette = PALETTE_SOLID_6
        elif n_sectors == 12:
            palette = PALETTE_SOLID_12
        elif n_sectors == 4:
            palette = PALETTE_SOLID_4
        else:
            angles = np.linspace(0, 179, n_sectors, endpoint=False, dtype=np.uint8)
            hsv_pal = np.stack([angles, np.full(n_sectors, 255, dtype=np.uint8), np.full(n_sectors, 255, dtype=np.uint8)], axis=-1)
            palette = cv2.cvtColor(hsv_pal.reshape(1, n_sectors, 3), cv2.COLOR_HSV2RGB).reshape(n_sectors, 3)

    palette = np.asarray(palette, dtype=np.uint8)
    n_colors = len(palette)

    arg = np.angle(w)
    arg = np.where(arg < 0, arg + 2 * np.pi, arg)
    arg_norm = (arg / (2 * np.pi) + hue_shift) % 1.0

    sector_idx = np.floor(arg_norm * n_colors).astype(np.int64) % n_colors
    rgb = palette[sector_idx]

    if mark_zeros_poles:
        mod = np.abs(w)
        rgb[mod < zero_threshold] = [0, 0, 0]        # Zeros em preto
        rgb[mod > pole_threshold] = [255, 255, 255]  # Polos em branco

    return rgb


def colorize_polar_chessboard(
    w: np.ndarray,
    n_sectors: int = 12,
    n_rings_scale: float = 2.0,
    color1: Tuple[int, int, int] = (245, 245, 245),
    color2: Tuple[int, int, int] = (30, 30, 30),
    hue_palette: Optional[np.ndarray] = None
) -> np.ndarray:
    """
    Coloração em Xadrez Polar com Cores Sólidas.
    Discretiza simultaneamente anéis concêntricos de log(|w|) e setores de arg(w).
    """
    arg = np.angle(w)
    arg = np.where(arg < 0, arg + 2 * np.pi, arg)
    sector_idx = np.floor((arg / (2 * np.pi)) * n_sectors).astype(np.int64)

    modulus = np.abs(w)
    log_mod = np.log(modulus + 1e-10)
    ring_idx = np.floor(log_mod * n_rings_scale).astype(np.int64)

    parity = (sector_idx + ring_idx) % 2

    if hue_palette is not None:
        hue_palette = np.asarray(hue_palette, dtype=np.uint8)
        c_idx = sector_idx % len(hue_palette)
        rgb = hue_palette[c_idx].copy()
        rgb[parity == 1] = (rgb[parity == 1] * 0.45).astype(np.uint8)
    else:
        rgb = np.zeros((*w.shape, 3), dtype=np.uint8)
        rgb[parity == 0] = color1
        rgb[parity == 1] = color2

    return rgb


# ==============================================================================
# MAPEAMENTO DE TEXTURA / IMAGEM ARBITRÁRIA NO PLANO W (IMAGE PULLBACK)
# ==============================================================================

def colorize_image_pullback(
    w: np.ndarray,
    texture: Union[str, Path, np.ndarray, Image.Image],
    u_range: Tuple[float, float] = (-2.5, 2.5),
    v_range: Tuple[float, float] = (-2.5, 2.5),
    border_mode: str = 'wrap',
    bg_color: Tuple[int, int, int] = (255, 255, 255),
    **kwargs
) -> np.ndarray:
    """
    Mapeia uma imagem arbitrária definida no plano w de volta para o plano z (Pullback Conforme f*(I)(z) = I(f(z))).

    Parâmetros:
        w: array complexo w = u + iv correspondente a f(z)
        texture: caminho para arquivo de imagem, PIL Image ou array numpy uint8 (H, W, 3)
        u_range: intervalo (u_min, u_max) no plano w coberto pela imagem
        v_range: intervalo (v_min, v_max) no plano w coberto pela imagem
        border_mode: modo de tratamento de borda/extensão ('wrap', 'clamp', 'mirror', 'constant')
        bg_color: cor RGB para pontos fora dos limites quando border_mode='constant'

    Retorna:
        Array RGB uint8 de mesma resolução espacial que w.
    """
    # Suporte a alias 'mode' retrocompatível
    mode = kwargs.get('mode', border_mode)
    if isinstance(texture, (str, Path)):
        tex_pil = Image.open(str(texture)).convert('RGB')
        tex_arr = np.array(tex_pil, dtype=np.uint8)
    elif isinstance(texture, Image.Image):
        tex_arr = np.array(texture.convert('RGB'), dtype=np.uint8)
    elif isinstance(texture, np.ndarray):
        if texture.ndim == 2:
            tex_arr = cv2.cvtColor(texture, cv2.COLOR_GRAY2RGB)
        elif texture.shape[2] == 4:
            tex_arr = cv2.cvtColor(texture, cv2.COLOR_RGBA2RGB)
        else:
            tex_arr = texture.copy()
    else:
        raise ValueError(f"Formato de textura inválido: {type(texture)}")

    tex_h, tex_w = tex_arr.shape[:2]
    u_min, u_max = u_range
    v_min, v_max = v_range

    u = np.real(w)
    v = np.imag(w)

    norm_u = (u - u_min) / (u_max - u_min)
    norm_v = (v_max - v) / (v_max - v_min)

    out_of_bounds = (norm_u < 0.0) | (norm_u > 1.0) | (norm_v < 0.0) | (norm_v > 1.0)

    if mode == 'wrap':
        norm_u = norm_u % 1.0
        norm_v = norm_v % 1.0
    elif mode == 'mirror':
        norm_u = np.abs((norm_u - 1.0) % 2.0 - 1.0)
        norm_v = np.abs((norm_v - 1.0) % 2.0 - 1.0)
    elif mode == 'clamp':
        norm_u = np.clip(norm_u, 0.0, 1.0)
        norm_v = np.clip(norm_v, 0.0, 1.0)
    elif mode == 'constant':
        norm_u = np.clip(norm_u, 0.0, 1.0)
        norm_v = np.clip(norm_v, 0.0, 1.0)

    map_x = (norm_u * (tex_w - 1)).astype(np.float32)
    map_y = (norm_v * (tex_h - 1)).astype(np.float32)

    rgb = cv2.remap(tex_arr, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

    if mode == 'constant':
        rgb[out_of_bounds] = bg_color

    return rgb


# ==============================================================================
# GERADORES DE TEXTURAS PARAMÉTRICAS PARA O PLANO W (SUPORTE A 4K / ALTA DENSIDADE)
# ==============================================================================

def generate_cartesian_grid_texture(
    size: Tuple[int, int] = (3840, 3840),
    grid_lines: int = 12,
    line_thickness: Optional[int] = None,
    axis_thickness: Optional[int] = None,
    bg_color: Tuple[int, int, int] = (252, 252, 254),
    grid_color: Tuple[int, int, int] = (40, 110, 200),
    axis_color: Tuple[int, int, int] = (225, 30, 30)
) -> np.ndarray:
    """Gera uma grade cartesiana com eixos coordenados em 4K e desenho suavizado."""
    w, h = size
    img = np.full((h, w, 3), bg_color, dtype=np.uint8)

    l_thick = line_thickness if line_thickness is not None else max(3, int(w * 0.004))
    a_thick = axis_thickness if axis_thickness is not None else max(6, int(w * 0.008))

    for i in range(grid_lines + 1):
        x = int(round(i * (w - 1) / grid_lines))
        y = int(round(i * (h - 1) / grid_lines))
        cv2.line(img, (x, 0), (x, h - 1), grid_color, l_thick, lineType=cv2.LINE_AA)
        cv2.line(img, (0, y), (w - 1, y), grid_color, l_thick, lineType=cv2.LINE_AA)

    cx, cy = w // 2, h // 2
    cv2.line(img, (cx, 0), (cx, h - 1), axis_color, a_thick, lineType=cv2.LINE_AA)
    cv2.line(img, (0, cy), (w - 1, cy), axis_color, a_thick, lineType=cv2.LINE_AA)

    return img


def generate_checkerboard_texture(
    size: Tuple[int, int] = (3840, 3840),
    squares_per_side: int = 10,
    color1: Tuple[int, int, int] = (250, 250, 252),
    color2: Tuple[int, int, int] = (25, 35, 55)
) -> np.ndarray:
    """Gera um tabuleiro de xadrez cartesiano de alta resolução para o plano w."""
    w, h = size
    img = np.zeros((h, w, 3), dtype=np.uint8)
    dx = w / squares_per_side
    dy = h / squares_per_side

    for r in range(squares_per_side):
        for c in range(squares_per_side):
            x1, y1 = int(round(c * dx)), int(round(r * dy))
            x2, y2 = int(round((c + 1) * dx)), int(round((r + 1) * dy))
            col = color1 if (r + c) % 2 == 0 else color2
            cv2.rectangle(img, (x1, y1), (x2, y2), col, -1)

    return img


def generate_concentric_targets_texture(
    size: Tuple[int, int] = (3840, 3840),
    n_rings: int = 10,
    colors: Optional[List[Tuple[int, int, int]]] = None
) -> np.ndarray:
    """Gera círculos concêntricos coloridos no plano w em 4K com anti-aliasing."""
    w, h = size
    img = np.full((h, w, 3), (255, 255, 255), dtype=np.uint8)
    cx, cy = w // 2, h // 2
    max_radius = min(cx, cy)

    if colors is None:
        colors = [
            (230,  30,  30),  # Vermelho
            (250, 185,   0),  # Amarelo
            ( 30, 180,  50),  # Verde
            (  0, 185, 230),  # Ciano
            ( 35,  75, 225),  # Azul
            (210,  30, 210),  # Magenta
        ]

    for i in range(n_rings, 0, -1):
        r = int(round(i * max_radius / n_rings))
        color = colors[(i - 1) % len(colors)]
        cv2.circle(img, (cx, cy), r, color, -1, lineType=cv2.LINE_AA)

    return img


def generate_truchet_texture(
    size: Tuple[int, int] = (3840, 3840),
    grid_size: int = 10,
    line_thickness: Optional[int] = None,
    bg_color: Tuple[int, int, int] = (250, 250, 252),
    line_color: Tuple[int, int, int] = (20, 40, 85)
) -> np.ndarray:
    """Gera um mosaico clássico de rosetas e arcos de Truchet em 4K com anti-aliasing."""
    w, h = size
    img = np.full((h, w, 3), bg_color, dtype=np.uint8)
    tile_w = w // grid_size
    tile_h = h // grid_size

    l_thick = line_thickness if line_thickness is not None else max(4, int(w * 0.014))

    np.random.seed(101)
    for r in range(grid_size):
        for c in range(grid_size):
            x0, y0 = c * tile_w, r * tile_h
            rot = (r * 3 + c * 7 + (r ^ c)) % 2
            rad = tile_w // 2

            if rot == 0:
                cv2.ellipse(img, (x0, y0), (rad, rad), 0, 0, 90, line_color, l_thick, lineType=cv2.LINE_AA)
                cv2.ellipse(img, (x0 + tile_w, y0 + tile_h), (rad, rad), 0, 180, 270, line_color, l_thick, lineType=cv2.LINE_AA)
            else:
                cv2.ellipse(img, (x0 + tile_w, y0), (rad, rad), 0, 90, 180, line_color, l_thick, lineType=cv2.LINE_AA)
                cv2.ellipse(img, (x0, y0 + tile_h), (rad, rad), 0, 270, 360, line_color, l_thick, lineType=cv2.LINE_AA)

    return img


# ==============================================================================
# CLASSE DE ALTO NÍVEL: DomainColoringEngine (SUPORTE NATIVO A 4K UHD)
# ==============================================================================

class DomainColoringEngine:
    """
    Motor Unificado de Coloração de Domínio para Funções Complexas com suporte a 4K UHD.
    """

    def __init__(
        self,
        func: Callable[[np.ndarray], np.ndarray],
        x_range: Tuple[float, float] = (-2.0, 2.0),
        y_range: Tuple[float, float] = (-2.0, 2.0),
        resolution: Tuple[int, int] = (3840, 3840)
    ):
        self.func = func
        self.x_range = x_range
        self.y_range = y_range
        self.resolution = resolution
        self._Z: Optional[np.ndarray] = None
        self._W: Optional[np.ndarray] = None

    def evaluate(self, force: bool = False) -> Tuple[np.ndarray, np.ndarray]:
        """Calcula ou recupera em cache a malha complexa Z e a imagem W = f(Z)."""
        if self._W is None or force:
            self._Z, self._W = evaluate_complex_grid(
                self.func, self.x_range, self.y_range,
                width=self.resolution[0], height=self.resolution[1]
            )
        return self._Z, self._W

    def render(self, mode: str = 'solid_sectors', **kwargs) -> Image.Image:
        """
        Renderiza a coloração de domínio no modo especificado.

        Modos suportados:
            - 'continuous': HSV clássico
            - 'solid_sectors': N setores de cores sólidas
            - 'wegert_enhanced': curvas de nível Wegert (módulo e fase)
            - 'polar_chessboard': xadrez polar com cores sólidas
            - 'cartesian_grid': pullback de grade cartesiana do plano w
            - 'checkerboard': pullback de xadrez cartesiano do plano w
            - 'concentric_targets': pullback de círculos concêntricos
            - 'truchet': pullback de mosaico de Truchet
            - 'custom_image': pullback de imagem arbitrária (requer kwargs['texture'])
        """
        _, W = self.evaluate()

        if mode == 'continuous':
            rgb = colorize_continuous_hsv(W, **kwargs)

        elif mode == 'solid_sectors':
            rgb = colorize_solid_sectors(W, **kwargs)

        elif mode == 'wegert_enhanced':
            rgb = colorize_wegert_enhanced(W, **kwargs)

        elif mode == 'polar_chessboard':
            rgb = colorize_polar_chessboard(W, **kwargs)

        elif mode == 'cartesian_grid':
            grid_tex = generate_cartesian_grid_texture(size=self.resolution)
            rgb = colorize_image_pullback(W, grid_tex, **kwargs)

        elif mode == 'checkerboard':
            check_tex = generate_checkerboard_texture(size=self.resolution)
            rgb = colorize_image_pullback(W, check_tex, **kwargs)

        elif mode == 'concentric_targets':
            target_tex = generate_concentric_targets_texture(size=self.resolution)
            rgb = colorize_image_pullback(W, target_tex, **kwargs)

        elif mode == 'truchet':
            truchet_tex = generate_truchet_texture(size=self.resolution)
            rgb = colorize_image_pullback(W, truchet_tex, **kwargs)

        elif mode == 'custom_image':
            if 'texture' not in kwargs:
                raise ValueError("Modo 'custom_image' requer o parâmetro 'texture'.")
            rgb = colorize_image_pullback(W, **kwargs)

        else:
            raise ValueError(f"Modo de coloração desconhecido: '{mode}'")

        return Image.fromarray(rgb)

    def generate_six_flexagon_faces(
        self,
        custom_texture: Optional[Union[str, Path, np.ndarray, Image.Image]] = None,
        custom_palette: Optional[np.ndarray] = None,
        texture_u_range: Tuple[float, float] = (-2.5, 2.5),
        texture_v_range: Tuple[float, float] = (-2.5, 2.5),
        texture_mode: str = 'wrap'
    ) -> Dict[str, Image.Image]:
        """Gera as 6 faces da coloração de domínio clássica/mista."""
        faces = {}
        faces['face1'] = self.render(mode='continuous', brightness_mode='balanced')
        faces['face2'] = self.render(mode='solid_sectors', n_sectors=6, palette=custom_palette if custom_palette is not None else PALETTE_SOLID_6)
        faces['face3'] = self.render(mode='wegert_enhanced', n_mod_lines=10, n_phase_lines=12, pattern_mode='both')
        faces['face4'] = self.render(mode='cartesian_grid', u_range=texture_u_range, v_range=texture_v_range, border_mode=texture_mode)
        if custom_texture is not None:
            faces['face5'] = self.render(mode='custom_image', texture=custom_texture, u_range=texture_u_range, v_range=texture_v_range, border_mode=texture_mode)
        else:
            faces['face5'] = self.render(mode='concentric_targets', n_rings=8, u_range=texture_u_range, v_range=texture_v_range, border_mode=texture_mode)
        faces['face6'] = self.render(mode='continuous', hue_shift=0.5, brightness_mode='balanced')
        return faces

    def generate_six_solid_faces(
        self,
        custom_palette: Optional[np.ndarray] = None,
        texture_u_range: Tuple[float, float] = (-2.5, 2.5),
        texture_v_range: Tuple[float, float] = (-2.5, 2.5),
        texture_mode: str = 'wrap'
    ) -> Dict[str, Image.Image]:
        """
        Gera 6 faces exclusivamente em CORES SÓLIDAS E PADRÕES GEOMÉTRICOS PÚROS (sem gradientes contínuos):
            Face 1: 6 Setores Angulares Sólidos (Hexacromático Puro)
            Face 2: Grade Cartesiana Ortogonal no Plano w (Pullback Conforme)
            Face 3: Tabuleiro de Xadrez Cartesiano no Plano w (Pullback Conforme)
            Face 4: Xadrez Polar Sólido (Discretização Setorial + Anéis)
            Face 5: Alvos Concêntricos em Cores Sólidas (Curvas de Nível)
            Face 6: Mosaico de Arcos de Truchet no Plano w (Pullback Conforme)
        """
        faces = {}

        # Face 1: 6 Setores Angulares Sólidos Puros
        faces['face1'] = self.render(
            mode='solid_sectors',
            n_sectors=6,
            palette=custom_palette if custom_palette is not None else PALETTE_SOLID_6
        )

        # Face 2: Grade Cartesiana Ortogonal (Pullback)
        faces['face2'] = self.render(
            mode='cartesian_grid',
            u_range=texture_u_range,
            v_range=texture_v_range,
            border_mode=texture_mode
        )

        # Face 3: Tabuleiro de Xadrez Cartesiano (Pullback)
        faces['face3'] = self.render(
            mode='checkerboard',
            u_range=texture_u_range,
            v_range=texture_v_range,
            border_mode=texture_mode
        )

        # Face 4: Xadrez Polar Sólido
        faces['face4'] = self.render(
            mode='polar_chessboard',
            n_sectors=12,
            n_rings_scale=2.0,
            color1=(250, 250, 250),
            color2=(25, 30, 45)
        )

        # Face 5: Círculos Concêntricos Sólidos (Alvos)
        faces['face5'] = self.render(
            mode='concentric_targets',
            n_rings=8,
            u_range=texture_u_range,
            v_range=texture_v_range,
            border_mode=texture_mode
        )

        # Face 6: Mosaico de Truchet Sólido (Pullback)
        faces['face6'] = self.render(
            mode='truchet',
            u_range=texture_u_range,
            v_range=texture_v_range,
            border_mode=texture_mode
        )

        return faces
