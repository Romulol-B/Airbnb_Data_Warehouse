-- “Bairros com mais reservas apresentam melhores notas de avaliação?”
-- (Comparação entre quantidade de reservas e notas médias consolidadas)


SELECT 
    loc.bairro,
    sum(r.total_reservas) as total_reservas,
    sum(r.faturamento) as total_faturamento,
    avg(a.nota_media) as nota_media
FROM
    -- Agrega a tabela de reservas
    (SELECT
        sk_imovel,
        sk_localizacao,
        sk_data,
        COUNT(*) AS total_reservas,
        SUM(preco) AS faturamento
     FROM fato_reservas
     GROUP BY sk_imovel, sk_localizacao, sk_data) r

JOIN
    -- Agrega a tabela de avaliações
    (SELECT
        sk_imovel,
        sk_localizacao,
        AVG(nota_media) AS nota_media
     FROM fato_avaliacao
     GROUP BY sk_imovel, sk_localizacao) a
ON  r.sk_imovel = a.sk_imovel
AND r.sk_localizacao = a.sk_localizacao

JOIN dim_localizacao loc ON loc.sk_localizacao = r.sk_localizacao
JOIN dim_data dt ON dt.sk_data = r.sk_data
GROUP BY loc.bairro
LIMIT 10000

