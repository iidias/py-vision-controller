# 🖐️ HandOS Lite (PyVision Controller)

Um sistema de controle gestual "touchless" desenvolvido em Python. Este projeto utiliza Visão Computacional e Inteligência Artificial para transformar uma webcam comum em um dispositivo de entrada futurista, permitindo controlar o mouse e jogar jogos apenas com movimentos das mãos no ar.

## 🧠 O que este projeto demonstra?

* **Visão Computacional (Computer Vision):** Uso do **OpenCV** para processamento de vídeo em tempo real e aplicação de filtros (Gaussian Blur).
* **Detecção de Pose (AI):** Utilização do **MediaPipe Hands** (Google) para inferência de 21 pontos esqueléticos (landmarks) da mão com alta precisão.
* **Matemática Vetorial:** Aplicação de Álgebra Linear e Geometria Euclidiana (`math.hypot`) para calcular distâncias entre dedos (gesto de pinça).
* **Suavização de Movimento:** Implementação do algoritmo **LERP (Linear Interpolation)** para remover a tremedeira natural da mão humana, garantindo um controle de mouse fluido.
* **Máquina de Estados:** Gerenciamento lógico de estados da aplicação (MENU vs. JOGANDO) com transições visuais.

## 🚀 Funcionalidades

### 1. 🖥️ Interface "Glassmorphism"
* Menu inicial interativo com efeito de desfoque (Blur) em tempo real.
* Reconhecimento de gestos para iniciar sem tocar no teclado (Gesto de "Paz e Amor" ✌️).

### 2. 🖱️ Mouse Virtual
* **Mover:** Levante o dedo indicador.
* **Clicar:** Junte o polegar com o indicador (gesto de pinça 🤏).
* **Área Útil:** Mapeamento inteligente que permite alcançar todos os cantos da tela movendo a mão apenas numa pequena área central da câmera.

### 3. 🏎️ Modo Gamer (Simulador de Corrida)
* **Acelerar (W):** Mão totalmente aberta (🖐️).
* **Frear (S):** Mão fechada (Punho ✊).
* *Ideal para jogos de corrida onde W acelera e S freia.*

## 🛠️ Requisitos e Instalação

### ⚠️ Avisos Importantes (Windows)
1. **Caminhos de Pasta:** O núcleo do MediaPipe (C++) não reconhece caminhos com **acentos, 'ç' ou caracteres especiais**.
   * ❌ **Não use:** `C:\Users\João\Downloads\Projeto`
   * ✅ **Use:** `C:\Projetos\HandOS` (Crie uma pasta na raiz do disco C).
2. **Versão do Python:** Utilize **Python 3.10 ou 3.11**. Versões mais recentes (3.12/3.13) ainda não são compatíveis.

### Passo a Passo

1. **Prepare o ambiente:**
   Crie uma pasta na raiz (ex: `C:\Projetos`) e coloque os arquivos lá.
2. **Crie um ambiente virtual (Recomendado): Isso evita conflitos com outras bibliotecas do sistema.**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```
3. **Instale as dependências:**
   ```bash
   pip install opencv-python mediapipe pyautogui numpy
   ```
4. **Execute o projeto:**
   ```bash
   python gestures_pro.py
   ```
## 🎮 Guia de Gestos

| Ação | Gesto | Estado |
| :--- | :--- | :--- |
| **Iniciar** | ✌️ (Sinal de V / Paz) | Menu |
| **Mover Cursor** | 👆 (Apenas Indicador levantado) | Jogo |
| **Clicar** | 🤏 (Pinça: Indicador + Dedão) | Jogo |
| **Acelerar (W)** | 🖐️ (Mão Aberta - 5 dedos) | Jogo |
| **Frear (S)** | ✊ (Mão Fechada - Punho) | Jogo |
| **Voltar ao Menu** | Tecla `M` | Jogo |
| **Sair** | Tecla `Q` | Qualquer |
