SELECT COUNT(0) FROM INDICADORES_RDNG WHERE QTDE_CCRC = '1' AND DATA_IMPORTACAO = '28/03/2023'
SELECT COUNT(0) FROM INDICADORES_RDNG WHERE QTDE_CCRC <> '1' AND DATA_IMPORTACAO = '28/03/2023'

SELECT count(0) FROM INDICADORES_RDNG where QTDE_NAO_RASTREADO is null

UPDATE INDICADORES_RDNG SET DATA_IMPORTACAO = '20230402' WHERE DATA_IMPORTACAO = '20230411'

SELECT INCLUSAO_REQ_CLEARCASE FROM INDICADORES_RDNG WHERE INCLUSAO_REQ_CLEARCASE <> '' and INCLUSAO_REQ_CLEARCASE <> 'None'


SELECT count(0) FROM INDICADORES_RDNG WHERE DATA_IMPORTACAO = '28/03/2023'

SELECT count(0) FROM INDICADORES_RDNG WHERE QTDE_RASTREADO = '1' AND DATA_IMPORTACAO = '27/03/2023'
SELECT count(0) FROM INDICADORES_RDNG WHERE QTDE_NAO_RASTREADO = '1' AND DATA_IMPORTACAO = '27/03/2023'


SELECT * FROM INDICADORES_RDNG WHERE QTDE_RASTREADO = '1' AND DATA_IMPORTACAO = '28/03/2023'
AND HU IN ( SELECT HU FROM INDICADORES_RDNG WHERE QTDE_RASTREADO <> '1' AND QTDE_NAO_RASTREADO <> '1')
AND DATA_IMPORTACAO = '27/03/2023'



SELECT INCLUSAO_REQ_CLEARCASE FROM INDICADORES_RDNG WHERE DATA_IMPORTACAO = '28/03/2023' AND INCLUSAO_REQ_CLEARCASE like '%MIGRA%' AND INCLUSAO_REQ_CLEARCASE not like '%01-REQ%'
SELECT INCLUSAO_REQ_CLEARCASE FROM INDICADORES_RDNG WHERE DATA_IMPORTACAO = '28/03/2023' AND INCLUSAO_REQ_CLEARCASE like '%01-REQ%' AND HU NOT IN (SELECT HU FROM INDICADORES_RDNG WHERE DATA_IMPORTACAO = '28/03/2023' AND INCLUSAO_REQ_CLEARCASE like '%MIGRA%')

SELECT INCLUSAO_REQ_CLEARCASE FROM INDICADORES_RDNG WHERE DATA_IMPORTACAO = '28/03/2023' AND (INCLUSAO_REQ_CLEARCASE like '%MIGRA%' OR INCLUSAO_REQ_CLEARCASE like '%01-REQ%')




SELECT DISTINCT(DATA_MODIF) , USUARIO , VOB
FROM PESQUISA_USUARIOS_REQ
WHERE DATA_MODIF > '2022-12-31'
GROUP BY USUARIO , VOB
ORDER BY USUARIO , VOB

delete from PESQUISA_USUARIOS_REQ where usuario = '1'



SELECT * FROM VOBs where TRIM(COMUNIDADE) = 'PESSOAS'

SELECT VOB, COMUNIDADE,FABRICA FROM VOBs

SELECT DISTINCT(GRUPO_COMPART) FROM COMPARTILHAMENTOS WHERE GRUPO_COMPART like '%ARRECADACAO%' AND GRUPO_COMPART like '%SPREAD%'
SELECT DISTINCT(GRUPO_COMPART) FROM COMPARTILHAMENTOS WHERE GRUPO_COMPART like '%CANAIS%' AND GRUPO_COMPART like '%SPREAD%'






SELECT  DISTINCT(COMPART.NOME_COMPART) AS VOB , VOBs.FABRICA AS FABRICA
FROM    COMPARTILHAMENTOS COMPART , VOBs
WHERE   GRUPO_COMPART like '%SEG%' 
AND     COMPART.NOME_COMPART = VOBs.VOB
ORDER BY COMPART.NOME_COMPART

SELECT VOB,FABRICA FROM VOBs WHERE COMUNIDADE like '%ARRECADACAO%' ORDER BY VOB

SELECT DISTINCT(VOB) AS VOB FROM VOBs where TRIM(COMUNIDADE) like '%ARRECADACAO%' ORDER BY VOB


SELECT * FROM VOBS WHERE VOB like "%SISGR%"
SELECT * FROM COMPARTILHAMENTOS WHERE NOME_COMPART like "%SISGR%"

UPDATE COMPARTILHAMENTOS SET NOME_COMPART = "SIGCB_ECOBRANÇA" where NOME_COMPART = "SIGCB_ECOBRAN€A"





SELECT  DISTINCT(COMPART.NOME_COMPART) AS VOB , VOBs.FABRICA AS FABRICA , VOBs.SERVIDOR FROM COMPARTILHAMENTOS COMPART,VOBs WHERE GRUPO_COMPART like '%ARRECADACAO%' AND COMPART.NOME_COMPART = VOBs.VOB ORDER BY COMPART.NOME_COMPART


SELECT  * FROM COMPARTILHAMENTOS WHERE GRUPO_COMPART like '%ARRECADACAO%'

SELECT  * FROM VOBs where VOB = 'SIEVJ'

SELECT  * FROM NET_SHARE


SELECT GRUPO_COMUNIDADE FROM GRUPOS_COMUNIDADE WHERE COMUNIDADE = ''


DELETE FROM GRUPOS_COMUNIDADE WHERE GRUPO_COMUNIDADE = "CORPCAIXA\G DF5222 CC_CAMBIO"