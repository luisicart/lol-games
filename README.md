# lol-games
 
Este repositório é um projeto pessoal, nascido de uma paixão por jogos e dados. Nele, busquei aprender sobre ingestão de dados via API com o intuíto de fornecer um modelo de Machine Learning com capacidades preditivas da vitória de um time.

Este projeto só foi possível devido a API aberta da desenvolvedora de jogos Riot Games. Caso queira saber mais, pode acessar a documentação neste link: [API Documentation](https://developer.riotgames.com/apis)

Quer saber mais? 

- [Sobre](#sobre)
    - [Contexto](#contexto)
    - [Etapas](#etapas)
    - [Setup](#setup)
- [Desafios](#desafios)
    - [Ingestão](#ingestao)
    - [Machine Learning](#machine-learning)

## Sobre

### Contexto

Desde pequeno sou apaixonado pelo mundo dos jogos, e aos 13 anos conheci o mundo dos jogos online através do League of Legends. 

> League of Legends (LoL) é um jogo multiplayer online de batalha em arena (MOBA), lançado em 2009 pela Riot Games. Nele, duas equipes de cinco jogadores competem para destruir a base inimiga, enquanto defendem a sua própria. Cada jogador controla um personagem chamado "campeão", que possui habilidades únicas e um papel específico na equipe, como causar dano, resistir a ataques ou dar suporte aos aliados. O mapa é dividido em três rotas principais: topo, meio e bot, além da selva. Durante a partida, os jogadores precisam derrotar inimigos e conquistar objetivos para acumular recursos que podem levar o time a vitória.

Desde então acompanho, mesmo que de longe, o cenário do jogo e seus campeonatos profissionais. Foi durante um desses campeonatos, o mundial de 2024, que durante a transmissão um gráfico me chamou atenção. Este gráfico era uma probabilidade de vitória de cada time de acordo com o tempo de jogo e recursos adquiridos pelos jogadores.

Minha paixão por jogos foi rapidamente substituída pela paixão por dados, surgindo a ideia de reproduzir as previsões demonstradas e algumas coisinhas a mais. 

Buscar por dados já extraídos seria o caminho mais fácil disponível, porém aproveitei este projeto para estudar um pouco mais sobre o consumo de dados por API. Esta não é minha especialidade e portanto estou sempre disposto a feedback de meu trabalho. 

Espero que goste deste projeto e se for replicá-lo, espero que divirta-se tanto quanto eu me diverti unindo minhas paixões de adulto e adolescente.

### Etapas

Este projeto possui duas etapas claras de desenvolvimento, ingestão e predição. Ambas serão realizadas em python e estarão dentro da pasta "src".

Para a ingestão dos dados utilizaremos a API pública disponibilizada pela desenvolvedora do jogo, Riot Games. Sendo ela pública e não de produção, possui limitações de *requests* e tempo, o que deve nos deixar atentos à quantos dados queremos utilizar.

Os dados extraídos serão somente os que acredito necessários ou interessantes para a produção de um modelo de Machine Learning e não estarão inicialmente no formato mais adequado para tal. Entre as etapas você irá se deparar com um processo de *feature engineering* onde tranformaremos os dados para o *input* no algoritimo.

Para saber mais sobre *feature engineering*: [Big Book of MLOps - Databricks](https://www.databricks.com/br/resources/ebook/the-big-book-of-mlops?scid=7018Y000001Fi0cQAC&utm_medium=paid+search&utm_source=google&utm_campaign=20613856692&utm_adgroup=159575945934&utm_content=ebook&utm_offer=the-big-book-of-mlops&utm_ad=696280074173&utm_term=mlops&gad_source=1&gclid=Cj0KCQjw3vO3BhCqARIsAEWblcAXbQ4jtLD3ndUhhgG8rcAHCvOB4nG6xYyKO0QqzZrv-bszsJCA_ewaAjOGEALw_wcB)

*Mais uma coisa, é provável que eu me aventure em algumas estatísticas de jogadores específicos (eu) como forma de acompanhamento. Você vai notar duas coisas, que eu não jogo muito e que sou muito ruim. Mas este arquivo também estará em "src" e terá uma etapa de ingestão única.*

### Setup 

Em meu projeto utilizei um ambiente virtual, que recomendo que o faça também:

```bash
python -m venv venv

./venv/Scripts/Activate
```
*O caminho venv está dentro do "gitignore" deste projeto.*

Além disso, todas as bibliotecas utilizadas neste projeto estão dentro do arquivo "requirements.txt" e você pode fazer a instalação completa em seu ambiente através do seguinte comando:

```bash
pip install -r requirements.txt
```

Por se tratar de uma API e de uma chave única de acesso, por motivos de segurança consta em meu projeto um arquivo ".env" que contem a variável "riot_api_key". Ela será utilizada para o acesso à API e também está presente no arquivo "gitignore".

## Desafios

### Ingestao

Esta etapa tem muitos desafios, especialmente para mim que não sou um engenheiro de dados. Vou me deter apenas em desafios que julgue elementar para entender o processo de execução e suas razões. Fique a vontade para me enviar um email ou mensagem caso tenha dúvida de etapas não mencionadas aqui.

**Ingestão de partidas:** 

Até o momento que estou escrevendo este arquivo a API da Riot Games não possui uma maneira de extrair partidas em geral de algum servidor ou região, a única maneira disponível é fazer a ingestão de partidas de um Jogador específico de cada vez.

Acredito que essa limitação seja proposital e faça com que tenhamos que criar novos caminhos. Particularmente achei muito bom pois pude praticar um pouco mais. Para este problema elenquei duas ideias e explicarei por que segui uma e não a outra.

1. A primeira ideia que tive era iniciar a extração dos dados de partidas de apenas um jogador, eu mesmo ou outro jogador melhor ranqueado. A partir destes dados, seria possível o acesso aos indentificadores de 9 outros jogadores, a cada partida, que o jogador inicial encontrou. Com novos *IDs* de jogadores poderiamos ampliar em cascata o encontro de novos históricos de partidas.
2. A segunda ideia e *escolhida*, utiliza a extração de partidas dos melhores joagores ranqueados do servidor. É possível a coleta destes dados através de outro *endpoint* da API. Essa estratégia foi escolhida pois estamos buscando prever os principais componentes que levam um time a vitória e utilizando os melhores jogadores estaremos reduzindo o viés de aprendizagem que partidas "comuns" podem ter. 

Para a ideia 2, é preciso primeiramente do *leader board* e depois a extração das partidas. Você verá esta estrutura no código.

### Machine Learning