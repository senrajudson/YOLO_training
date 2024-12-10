Aqui está a lista com a soma final ajustada para o peso 2 no critério de "resultado". A organização é mantida por grupos, com a ordem decrescente dentro de cada grupo:

---

### **1. Transformações de Nitidez e Desfoque**
- **GaussianBlur (3, 4, 5)**: **Soma: 17**  
  Pouco mais complexo, risco baixo, resultado excelente.
- **MotionBlur (3, 4, 5)**: **Soma: 17**  
  Moderadamente complexo, risco baixo, ótimo para simular movimento.
- **UnsharpMask (3, 4, 5)**: **Soma: 17**  
  Complexidade média, risco moderado de artefatos, bom para detalhes.
- **Blur (4, 5, 4)**: **Soma: 17**  
  Simples, baixo risco, bom para suavizar.
- **MedianBlur (3, 5, 4)**: **Soma: 16**  
  Simples, baixo risco, bom para suavização local.
- **Sharpen (4, 4, 4)**: **Soma: 16**  
  Simples, moderado risco de over-sharpening, bom para nitidez.
- **AdvancedBlur (2, 3, 5)**: **Soma: 15**  
  Mais complexo, risco de distorção maior, mas resultados avançados.

---

### **2. Transformações de Contraste e Tons**
- **AutoContrast (5, 5, 5)**: **Soma: 20**  
  Muito simples, risco mínimo, ótimo para contraste.
- **RandomBrightnessContrast (4, 4, 5)**: **Soma: 17**  
  Simples, controle fácil de parâmetros.
- **RandomGamma (4, 4, 5)**: **Soma: 17**  
  Semelhante ao brilho/contraste com leve variação.
- **CLAHE (4, 4, 5)**: **Soma: 17**  
  Moderadamente simples, resultados robustos para áreas com pouca luz.
- **Equalize (4, 5, 4)**: **Soma: 17**  
  Simples, baixo risco, mas efeitos podem ser sutis.
- **PlasmaBrightnessContrast (3, 3, 5)**: **Soma: 14**  
  Mais complexo, mas produz variações criativas.
- **Solarize (4, 3, 4)**: **Soma: 14**  
  Simples, risco moderado devido à inversão parcial.

---

### **3. Transformações de Cores**
- **ToGray (5, 5, 5)**: **Soma: 20**  
  Simples, resultado confiável.
- **ToRGB (5, 5, 5)**: **Soma: 20**  
  Conversão direta para RGB, ideal para uniformidade.
- **HueSaturationValue (4, 4, 5)**: **Soma: 17**  
  Simples, baixo risco, ajusta matiz e saturação bem.
- **RGBShift (4, 3, 5)**: **Soma: 16**  
  Simples, mas pode criar cores irreais.
- **ColorJitter (4, 3, 5)**: **Soma: 16**  
  Boa para variação, mas pode distorcer o dataset.
- **ToSepia (5, 5, 4)**: **Soma: 18**  
  Semelhante ao cinza, mas com um tom artístico.
- **FancyPCA (3, 3, 4)**: **Soma: 14**  
  Mais técnica, útil para diversidade de cor.

---

### **4. Ruído e Textura**
- **ISONoise (3, 4, 5)**: **Soma: 17**  
  Simula bem ruído de câmeras digitais.
- **ShotNoise (3, 4, 5)**: **Soma: 17**  
  Semelhante ao ISO, com aplicação mais direta.
- **AdditiveNoise (4, 4, 4)**: **Soma: 16**  
  Simples, bom para generalização.
- **SaltAndPepper (4, 4, 4)**: **Soma: 16**  
  Clássico para teste de robustez.
- **MultiplicativeNoise (3, 4, 4)**: **Soma: 15**  
  Menos comum, mas útil em casos específicos.

---

### **5. Artefatos e Degradação**
- **ImageCompression (5, 5, 5)**: **Soma: 20**  
  Simples e eficaz para simular compressão.
- **Posterize (5, 5, 4)**: **Soma: 18**  
  Reduz tons para criar um efeito estilizado.
- **Downscale (5, 5, 4)**: **Soma: 18**  
  Simula baixa resolução de forma simples.
- **RingingOvershoot (3, 3, 4)**: **Soma: 14**  
  Menos comum, mas útil para artefatos específicos.

---

### **6. Efeitos Naturais**
- **RandomFog (4, 4, 5)**: **Soma: 17**  
  Realista para cenários de baixa visibilidade.
- **RandomSnow (4, 4, 5)**: **Soma: 17**  
  Simula neve bem.
- **RandomRain (4, 4, 5)**: **Soma: 17**  
  Simula chuva com controle de intensidade.
- **RandomShadow (4, 4, 5)**: **Soma: 17**  
  Simula sombras de forma realista.
- **RandomSunFlare (3, 4, 5)**: **Soma: 17**  
  Mais complexo, mas gera um bom efeito.

---

### **7. Distorções e Transformações Avançadas**
- **ChromaticAberration (3, 4, 5)**: **Soma: 17**  
  Simula aberração cromática realista.
- **Defocus (3, 4, 5)**: **Soma: 17**  
  Bom para simular desfoque.
- **GlassBlur (2, 3, 5)**: **Soma: 15**  
  Complexo, mas útil para distorções específicas.
- **HistogramMatching (3, 3, 5)**: **Soma: 14**  
  Combina distribuições de cor com outra imagem.
- **PixelDistributionAdaptation (3, 3, 4)**: **Soma: 13**  
  Semelhante, mas aplicado no nível de pixel.
- **PlasmaShadow (3, 4, 4)**: **Soma: 15**  
  Efeito criativo com sombras.

---

### **8. Alterações Estruturais**
- **RandomToneCurve (3, 4, 5)**: **Soma: 17**  
  Ajusta curvas de tom para diversidade.
- **Superpixels (4, 4, 4)**: **Soma: 16**  
  Reduz a imagem para blocos estruturais.
- **Emboss (4, 3, 4)**: **Soma: 15**  
  Adiciona relevo visual.
- **Spatter (3, 3, 4)**: **Soma: 14**  
  Simula respingos ou manchas.

---

### **9. Transformações Auxiliares**
- **FromFloat (5, 5, 5)**: **Soma: 20**  
  Conversão direta, simples e confiável.
- **ToFloat (5, 5, 5)**: **Soma: 20**  
  Simples e útil para pre-processamento.
- **InvertImg (5, 5, 5)**: **Soma: 20**  
  Inverte cores de forma confiável.

---

Aqui está uma breve descrição de cada transformação da biblioteca Albumentations:

1. **AdditiveNoise**: Adiciona ruído aleatório à imagem, simulando interferência.
2. **AdvancedBlur**: Aplica diferentes tipos de desfoque avançado na imagem.
3. **AutoContrast**: Ajusta automaticamente o contraste da imagem.
4. **Blur**: Aplica um desfoque simples à imagem.
5. **CLAHE**: Melhora o contraste usando Equalização de Histograma Limitada por Contraste.
6. **ChannelDropout**: Remove aleatoriamente canais de cor (como R, G ou B).
7. **ChannelShuffle**: Mistura a ordem dos canais de cor na imagem.
8. **ChromaticAberration**: Simula aberração cromática, criando bordas coloridas em áreas de contraste.
9. **ColorJitter**: Ajusta brilho, contraste, saturação e matiz de forma aleatória.
10. **Defocus**: Simula desfoque de foco.
11. **Downscale**: Reduz a resolução da imagem para simular qualidade inferior.
12. **Emboss**: Aplica um efeito de relevo à imagem.
13. **Equalize**: Equaliza o histograma da imagem, melhorando contraste.
14. **FDA**: Adapta a distribuição de cores de uma imagem de referência.
15. **FancyPCA**: Modifica as cores da imagem usando Análise de Componentes Principais (PCA).
16. **FromFloat**: Converte imagens em ponto flutuante para inteiros.
17. **GaussianBlur**: Aplica um desfoque gaussiano à imagem.
18. **GlassBlur**: Simula distorções similares a olhar através de vidro.
19. **HistogramMatching**: Ajusta a distribuição de cores para combinar com uma imagem de referência.
20. **HueSaturationValue**: Ajusta o matiz, a saturação e o valor da imagem.
21. **ISONoise**: Simula ruído ISO, como o de câmeras digitais.
22. **Illumination**: Altera o brilho para simular condições de iluminação diferentes.
23. **ImageCompression**: Simula compressão JPEG, reduzindo qualidade.
24. **InvertImg**: Inverte as cores da imagem.
25. **MedianBlur**: Aplica um desfoque usando a mediana dos pixels vizinhos.
26. **MotionBlur**: Simula desfoque causado por movimento.
27. **MultiplicativeNoise**: Adiciona ruído multiplicativo à imagem.
28. **Normalize**: Normaliza os valores de pixel (por exemplo, para redes neurais).
29. **PixelDistributionAdaptation**: Adapta a distribuição dos pixels para parecer com uma imagem de referência.
30. **PlanckianJitter**: Altera a temperatura de cor para simular condições de luz realistas.
31. **PlasmaBrightnessContrast**: Ajusta brilho e contraste com base em padrões de plasma.
32. **PlasmaShadow**: Adiciona sombras baseadas em padrões de plasma.
33. **Posterize**: Reduz o número de tons de cor na imagem.
34. **RGBShift**: Altera os valores dos canais RGB individualmente.
35. **RandomBrightnessContrast**: Ajusta brilho e contraste aleatoriamente.
36. **RandomFog**: Simula névoa na imagem.
37. **RandomGamma**: Altera os valores gama para modificar o brilho.
38. **RandomGravel**: Adiciona texturas de cascalho ou partículas.
39. **RandomRain**: Simula chuva na imagem.
40. **RandomShadow**: Adiciona sombras aleatórias na imagem.
41. **RandomSnow**: Simula neve na imagem.
42. **RandomSunFlare**: Adiciona efeitos de brilho do sol.
43. **RandomToneCurve**: Ajusta as curvas de tom da imagem.
44. **RingingOvershoot**: Simula artefatos de nitidez excessiva.
45. **SaltAndPepper**: Adiciona ruído de sal e pimenta (pixels pretos e brancos aleatórios).
46. **Sharpen**: Aumenta a nitidez da imagem.
47. **ShotNoise**: Adiciona ruído de disparo, como o ruído de sensores de câmera.
48. **Solarize**: Inverte parcialmente as cores com base em um limite de intensidade.
49. **Spatter**: Simula respingos ou manchas.
50. **Superpixels**: Reduz os detalhes da imagem dividindo-a em superpixels.
51. **TemplateTransform**: Transforma a imagem com base em um modelo específico.
52. **TextImage**: Adiciona texto na imagem.
53. **ToFloat**: Converte valores inteiros de pixel em ponto flutuante.
54. **ToGray**: Converte a imagem para escala de cinza.
55. **ToRGB**: Converte imagens de escala de cinza ou outros formatos para RGB.
56. **ToSepia**: Aplica um efeito de sépia à imagem.
57. **UnsharpMask**: Aumenta a nitidez realçando os detalhes.
58. **ZoomBlur**: Aplica um desfoque radial, simulando zoom em movimento.

