# -*- coding: utf-8 -*-
"""
Conjuntos em Jogo
=================
Quiz educativo de Matemática Discreta sobre definição de conjuntos,
união, interseção, complemento e subconjuntos.

Execute com:
    python main.py
"""

import json
import os
import sys

import pygame

from jogo import config as cfg
from jogo import ui
from jogo.telas import TelaInstrucoes, TelaMenu, TelaQuiz, TelaResultado


class Jogo:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.display.set_caption("Conjuntos em Jogo — Quiz de Matemática Discreta")

        self.tela = pygame.display.set_mode((cfg.LARGURA, cfg.ALTURA))
        self.relogio = pygame.time.Clock()
        self.rodando = True
        self.transicao = 0.0

        self.imagens = self._carregar_imagens()
        pygame.display.set_icon(self.imagens["logo.png"])
        self.sons = self._carregar_sons()

        self.recorde = self._ler_recorde()
        self.novo_recorde = False

        self.tela_atual = TelaMenu(self)

    # -- carregamento ------------------------------------------------------
    def _carregar_imagens(self):
        nomes = [
            "fundo.png", "logo.png", "cartao_instrucoes.png",
            "venn_uniao.png", "venn_intersecao.png", "venn_complemento.png",
            "venn_diferenca.png", "venn_subconjunto.png", "venn_disjuntos.png",
            "venn_dois_conjuntos.png",
        ]
        return {nome: cfg.imagem(nome) for nome in nomes}

    def _carregar_sons(self):
        sons = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            for nome in ("clique", "acerto", "erro", "fim", "tempo"):
                som = cfg.som(nome + ".wav")
                som.set_volume(0.55 if nome != "clique" else 0.35)
                sons[nome] = som
        except pygame.error:
            # sem placa de som: o jogo continua funcionando em silêncio
            sons = {}
        return sons

    def _ler_recorde(self):
        try:
            with open(cfg.ARQUIVO_RECORDE, "r", encoding="utf-8") as arquivo:
                return int(json.load(arquivo).get("recorde", 0))
        except (OSError, ValueError, TypeError):
            return 0

    def _gravar_recorde(self):
        try:
            with open(cfg.ARQUIVO_RECORDE, "w", encoding="utf-8") as arquivo:
                json.dump({"recorde": self.recorde}, arquivo)
        except OSError:
            pass

    # -- navegação ---------------------------------------------------------
    def ir_para(self, tela):
        self.tela_atual = tela
        self.transicao = 1.0

    def mostrar_menu(self):
        self.ir_para(TelaMenu(self))

    def mostrar_instrucoes(self):
        self.ir_para(TelaInstrucoes(self))

    def iniciar_jogo(self):
        self.ir_para(TelaQuiz(self))

    def mostrar_resultado(self, dados):
        if dados["pontos"] > self.recorde:
            self.recorde = dados["pontos"]
            self.novo_recorde = True
            self._gravar_recorde()
        else:
            self.novo_recorde = False
        self.ir_para(TelaResultado(self, dados))
        self.tocar("fim")

    def encerrar(self):
        self.rodando = False

    def tocar(self, nome):
        if nome in self.sons:
            self.sons[nome].play()

    # -- laço principal ----------------------------------------------------
    def executar(self):
        while self.rodando:
            dt = min(self.relogio.tick(cfg.FPS) / 1000.0, 0.05)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                else:
                    self.tela_atual.tratar_evento(evento)

            self.tela_atual.atualizar(dt)
            self.tela_atual.desenhar(self.tela)

            if self.transicao > 0:
                self.transicao = max(0.0, self.transicao - dt * 4.5)
                camada = pygame.Surface((cfg.LARGURA, cfg.ALTURA))
                camada.fill((18, 18, 40))
                camada.set_alpha(int(255 * self.transicao))
                self.tela.blit(camada, (0, 0))

            pygame.display.flip()

        pygame.quit()
        sys.exit(0)


def main():
    Jogo().executar()


if __name__ == "__main__":
    main()
