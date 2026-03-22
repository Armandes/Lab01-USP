# Lab01-USP
## Aluno: João Armandes Vieira Costa
### Bibliotecas desta atividade:
(usar -> pip install pandas seaborn matplotlib pyarrow sqlalchemy dotenv psycopg2)
- Pandas -> Edição das tabelas do database
- Seaborn -> Criação de gráficos
- Matplotlib -> Criação de gráficos
- Pyarrow -> Criação do Parquet
- Sqlachemy -> Usar SQL
- dotenv -> Manutenção do arquivo .env
- psycopg2 -> Habilita operações de SQL

### Arquitetura
Na camada raw existe o arquivo *gaming_mental_health_database*, em scripts/01_bronze.py temos um código que cria um log
checando se está tudo certo com a base.
Após vermos que a base de dados está tudo certo, na camada silver checamos se os dados
nessa base estão todos ok, limpamos e criamos o parquet.
O parquet é usado para eficiência maior para lidar com tudo.
Após criado o parquet, criamos alguns gráficos para verificar informações relevantes também.
Depois, na camada gold importamos a base para o Pòstgres e finalmente conseguimos fazer operações de SQL.

#### Dados das tabelas:
#### Tabela dim_comportamento
- player_id -> ID do jogador
- multiplayer_ratio -> razão de jogatinas multiplayer
- toxic_exposure -> exposição a ambientes de jogos tóxicos
- violent_games_ratio -> razão de jogatinas de jogos violentos
- mobile_gaming_ratio -> razão de jogatinas mobile
- night_gaming_ratio -> razão de jogatinas durante a noite
- esports_interest -> razão de interesse por jogos de e-sport
- headset_usage -> Usa headset (sim/não)
- microtransactions_spending -> Quanto já gastou em microtransações
- competitive_rank -> ranking competitivo
- internet_quality -> qualidade da internet

#### Tabela dim_habitos
- daily_gaming_hours -> Horas diárias de jogatina
- weekly_sessions -> Sessões de jogo na semana
- years_gaming -> Anos que joga
- sleep_hours -> Média de horas/dia
- caffeine_intake -> quantidade de cafeína ingerida
- exercise_hours -> horas de exercício por dia
- weekend_gaming_hours -> horas jogadas nos fins de semana
- screen_time_total -> total de tempo de tela
- streaming_hours -> horas assistindo streamings

#### Tabela dim_jogador
- age -> idade
- gender -> gênero
- income -> salário/ano
- bmi -> IMC

#### Tabela dim_social
- friends_gaming_count -> Quantidade de amigos que jogam
- online_friends -> Quantidade de amigos online
- social_interaction_score -> Score de interação
- relationship_satisfaction -> Score de satisfação com o relacionamento
- loneliness_score -> Score de solidão
- parental_supervision -> Tem supervisão parental?

#### Tabela fato_saude_mental
- stress_level -> score de estresse
- anxiety_score -> score de ansiedade
- depression_score -> score de depressão
- addiction_level -> nível de vício
- happiness_score -> score de felicidade
- aggresion_score -> score de agressividade
- academic_performance -> score de performance acadêmico
- work_productivity -> produtividade no trabalho
- eye_strain_score -> Score de cansaço ocular
- back_pain_score -> Score de dor na coluna

### Modo de modelagem:
Star schema, no arquivo gold/carga.py, onde também vamos carregar para o Postgres

Tabela fato:
fato_saude_mental -> Dados sobre estresse, performance acadêmica, depressão, etc

Tabelas de dimensão:
- dim_social -> Dados sobre interações do jogador e amizades
- dim_comportamento -> dados sobre interesses, comportamentos e gostos
- dim_habitos -> Dados sobre as sessões de jogo e rotinas do jogador
- dim_jogador -> Dados sobre o jogador

*o player ID é o PK em todas as tabelas.

### Rodar checagem da database e criar um log em data/raw: 
python scripts/01_bronze.py

### Rodar checagem geral dos dados e criar um log (no terminal mesmo): 
python data/silver/check.py

### Criar o arquivo .mk da análise dos dados:
python data/silver/graphics.py

### Carregar para o banco de dados já no formato Star Schema:
python data/gold/carga.py

### Puxar informações relevantes para análise de dados
python data/gold/metricas.py

### Ordem de execução dos arquivos:
1. scripts/01_bronze.py
2. data/silver/check.py
3. data/silver/cleaning.py
4. data/silver/graphics.py -> Como essa etapa consome o parquet, é essencial rodar as etapas anteriores. 
5. data/gold/carga.py -> Aqui puxamos os dados já do banco
6. data/gold/metricas.py


### Dificuldades encontradas:
- Entendimento do Star Schema e como criá-lo na prática.
- Conexão com o banco.
- O database em si não tinha muitos problemas, mas precisei fazer algumas operações para assegurar que estava tudo certo por precaução.

