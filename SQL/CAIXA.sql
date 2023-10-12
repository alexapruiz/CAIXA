use CAIXA

select * from Demandas_BRQ
select 123+'abc' as result
select	D.ID, D.QTDE, D.COMPLEXIDADE,
		S.COMPLEXIDADE_BAIXA, S.COMPLEXIDADE_MEDIA,S.COMPLEXIDADE_ALTA
from	Demandas_BRQ D , Servicos S
where	D.SERVICO = S.SERVICO

select	PERIODO, sum(UST) as USTs from	Demandas_BRQ where	PERIODO is not null group by PERIODO ORDER BY PERIODO

select	sum(UST) as USTs, PERIODO , FERRAMENTA
from	Demandas_BRQ
where	GRUPO = 'Grupo 2'
group	by PERIODO , FERRAMENTA
order	by PERIODO , FERRAMENTA , USTs


BULK INSERT AREAS_RDNG
FROM 'C:\Projetos\Python\Exemplos\Listas\areas_rdng_raw.txt'
WITH
(
    FIRSTROW = 1, -- as 1st one is header
    FIELDTERMINATOR = ';',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    TABLOCK
)

SELECT * FROM SAIDA
SELECT * FROM AREAS_RTC
SELECT * FROM AREAS_RDNG

SELECT * from AREAS_RDNG
where	substring(AREA_RDNG,2,5) NOT IN (SELECT substring(AREA_RDNG,1,5) FROM SAIDA)

SELECT * from AREAS_RTC
where	substring(AREA_RTC,2,5) NOT IN (SELECT substring(AREA_RTC,1,5) FROM SAIDA)

SELECT * from saida where AREA_RTC like 'SI003'

SELECT DISTINCT(AREA_RTC) FROM SAIDA


--- Vitrine
DROP TABLE USUARIOS_VITRINE
create table USUARIOS_VITRINE (USUARIO varchar(7) , NOME_USUARIO varchar(100), FUNCAO varchar(100))

BULK INSERT USUARIOS_VITRINE
FROM 'C:\Users\Alex\Downloads\Cominidade Vitrine.csv'
WITH
(
    FIRSTROW = 2, -- as 1st one is header
    FIELDTERMINATOR = ';',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    TABLOCK
)

--TRUNCATE TABLE USUARIOS_VITRINE
SELECT DISTINCT * FROM USUARIOS_VITRINE ORDER BY FUNCAO , USUARIO


--Listas
select AREA_RTC as AREA from AREAS_RTC where substring(AREA_RTC,1,3) like ' SI'
union
select AREA_RDNG as AREA from AREAS_RDNG where substring(AREA_RDNG,1,3) like ' SI'
order by AREA

----------------------------------------------------------------
-- SLA
select	*
from	Demandas_SLA

select * from Demandas_SLA where ID_RTC = 16228144 and status = 'Rejeitado'

select	*
from	Resumo_Demandas_SLA
where id in ( select distinct(id_rtc) from Demandas_SLA where status = 'Cancelado')

select count(0) as ATRASADAS from Resumo_Demandas_SLA WHERE PERIODO = '2021/01' and ATRASADO = 1
select count(0) as ESTOQUE from Resumo_Demandas_SLA WHERE PERIODO = '2021/01' and ESTOQUE = 1
select count(0) as REJEITADAS from Resumo_Demandas_SLA WHERE PERIODO = '2021/01' and REJEITADO = 1

----------------------------------------------------------------



select * from Demandas_BRQ where ID = 1522235

update Demandas_BRQ set Preposto = 'Alex Ap Ruiz' where id = 1522235





select * from cliente

insert into cliente (codigo , nome ) values (2,'cliente 2')
insert into cliente (codigo , nome ) values (3,'cliente 3')
insert into cliente (codigo , nome ) values (6,'cliente aaaa')


select ROW_NUMBER() OVER (order by nome) as row_num , nome from cliente

select * from cliente