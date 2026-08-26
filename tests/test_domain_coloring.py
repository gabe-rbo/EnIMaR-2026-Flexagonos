"""
Testes unitários e de integração para o motor de Coloração de Domínio (domain_coloring.py).
"""

import sys
from pathlib import Path
import unittest
import numpy as np
from PIL import Image

# Adicionar pastas do src ao sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src" / "visualization"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src" / "fabrication"))

from domain_coloring import (
    evaluate_complex_grid,
    colorize_continuous_hsv,
    colorize_wegert_enhanced,
    colorize_solid_sectors,
    colorize_polar_chessboard,
    colorize_image_pullback,
    generate_cartesian_grid_texture,
    generate_checkerboard_texture,
    DomainColoringEngine,
    PALETTE_SOLID_6,
    PALETTE_SOLID_4
)


class TestDomainColoring(unittest.TestCase):

    def test_evaluate_complex_grid_basic(self):
        """Verifica a criação da malha e avaliação de f(z) = z."""
        func = lambda z: z
        Z, W = evaluate_complex_grid(func, x_range=(-2, 2), y_range=(-1, 1), width=100, height=50)
        self.assertEqual(Z.shape, (50, 100))
        self.assertEqual(W.shape, (50, 100))
        # No canto superior esquerdo (linha 0, col 0): x=-2, y=1 -> z = -2 + 1j
        np.testing.assert_almost_equal(Z[0, 0], -2.0 + 1.0j)
        # No canto inferior direito (linha 49, col 99): x=2, y=-1 -> z = 2 - 1j
        np.testing.assert_almost_equal(Z[-1, -1], 2.0 - 1.0j)

    def test_evaluate_complex_grid_singularities(self):
        """Verifica tratamento seguro de singularidades como 1/z em z=0."""
        func = lambda z: 1.0 / z
        Z, W = evaluate_complex_grid(func, x_range=(-1, 1), y_range=(-1, 1), width=51, height=51)
        self.assertFalse(np.isnan(W).any())
        self.assertFalse(np.isinf(W).any())

    def test_colorize_solid_sectors(self):
        """Verifica se a coloração por cores sólidas usa estritamente as cores da paleta."""
        func = lambda z: z
        _, W = evaluate_complex_grid(func, x_range=(-2, 2), y_range=(-2, 2), width=60, height=60)
        rgb = colorize_solid_sectors(W, n_sectors=6, palette=PALETTE_SOLID_6, mark_zeros_poles=False)
        
        self.assertEqual(rgb.shape, (60, 60, 3))
        self.assertEqual(rgb.dtype, np.uint8)

        # Todas as cores presentes na imagem devem pertencer à PALETTE_SOLID_6
        unique_colors = np.unique(rgb.reshape(-1, 3), axis=0)
        for u_col in unique_colors:
            matches = np.all(PALETTE_SOLID_6 == u_col, axis=1)
            self.assertTrue(np.any(matches), f"Cor {u_col} não pertence à paleta de 6 cores sólidas!")

    def test_colorize_solid_sectors_angles(self):
        """Testa o mapeamento angular exato dos 4 quadrantes."""
        # Ângulos: 0° (eixo +X), 90° (+Y), 180° (-X), 270° (-Y)
        test_pts = np.array([[1.0 + 0j, 0.0 + 1j], [-1.0 + 0j, 0.0 - 1j]])
        rgb = colorize_solid_sectors(test_pts, n_sectors=4, palette=PALETTE_SOLID_4, mark_zeros_poles=False)
        
        np.testing.assert_array_equal(rgb[0, 0], PALETTE_SOLID_4[0])  # 0° -> Q1
        np.testing.assert_array_equal(rgb[0, 1], PALETTE_SOLID_4[1])  # 90° -> Q2
        np.testing.assert_array_equal(rgb[1, 0], PALETTE_SOLID_4[2])  # 180° -> Q3
        np.testing.assert_array_equal(rgb[1, 1], PALETTE_SOLID_4[3])  # 270° -> Q4

    def test_colorize_continuous_hsv(self):
        """Testa geração do mapa contínuo HSV em diferentes modos de brilho."""
        func = lambda z: (z - 1) / (z**2 + z + 1)
        _, W = evaluate_complex_grid(func, width=40, height=40)
        
        for b_mode in ['constant', 'log_modulus', 'balanced']:
            rgb = colorize_continuous_hsv(W, brightness_mode=b_mode)
            self.assertEqual(rgb.shape, (40, 40, 3))
            self.assertEqual(rgb.dtype, np.uint8)
            self.assertTrue((rgb >= 0).all() and (rgb <= 255).all())

    def test_colorize_wegert_enhanced(self):
        """Testa geração de linhas de nível e polar tiles de Wegert."""
        func = lambda z: z**3 - 1
        _, W = evaluate_complex_grid(func, width=50, height=50)
        
        for mode in ['modulus', 'phase', 'both', 'polar_tiles']:
            rgb = colorize_wegert_enhanced(W, n_mod_lines=8, n_phase_lines=12, pattern_mode=mode)
            self.assertEqual(rgb.shape, (50, 50, 3))
            self.assertEqual(rgb.dtype, np.uint8)

    def test_image_pullback_conformal(self):
        """Testa o pullback conforme com rotação e escala."""
        # Criar imagem teste 100x100 com 4 blocos de cores
        tex = np.zeros((100, 100, 3), dtype=np.uint8)
        tex[:50, :50] = [255, 0, 0]    # Top-Left: Vermelho
        tex[:50, 50:] = [0, 255, 0]    # Top-Right: Verde
        tex[50:, :50] = [0, 0, 255]    # Bottom-Left: Azul
        tex[50:, 50:] = [255, 255, 0]  # Bottom-Right: Amarelo

        # Identidade f(z) = z sobre [-1, 1]x[-1, 1]
        _, W_id = evaluate_complex_grid(lambda z: z, x_range=(-1, 1), y_range=(-1, 1), width=100, height=100)
        res_id = colorize_image_pullback(W_id, tex, u_range=(-1, 1), v_range=(-1, 1), mode='clamp')
        self.assertEqual(res_id.shape, (100, 100, 3))
        
        # Testar cantos mapeados corretamente
        # Top-left (z = -1 + 1j) -> tex Top-Left (Vermelho)
        self.assertAlmostEqual(res_id[5, 5, 0], 255, delta=10)
        self.assertAlmostEqual(res_id[5, 5, 1], 0, delta=10)
        # Top-right (z = 1 + 1j) -> tex Top-Right (Verde)
        self.assertAlmostEqual(res_id[5, 95, 1], 255, delta=10)

    def test_domain_coloring_solid_faces(self):
        """Testa a geração das 6 faces exclusivamente em cores sólidas."""
        func = lambda z: (z - 1) / (z**2 + z + 1)
        engine = DomainColoringEngine(func, x_range=(-2, 2), y_range=(-2, 2), resolution=(64, 64))
        
        faces = engine.generate_six_solid_faces()
        self.assertEqual(len(faces), 6)
        for i in range(1, 7):
            key = f'face{i}'
            self.assertIn(key, faces)
            self.assertIsInstance(faces[key], Image.Image)
            self.assertEqual(faces[key].size, (64, 64))


if __name__ == '__main__':
    unittest.main()
