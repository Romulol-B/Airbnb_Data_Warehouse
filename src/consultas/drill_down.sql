-- Mostre a nota média geral de avaliação para um bairro. Em seguida, detalhe essa nota por tipo de propriedade.

SELECT
    t2.bairro,
    t3.tipo_propriedade,
    COUNT(*) AS quantidade_imoveis,
    AVG(t1.nota_media) AS nota_media_bairro
FROM
    fato_avaliacao t1
JOIN dim_localizacao t2
    ON t1.sk_localizacao = t2.sk_localizacao
JOIN dim_imoveis t3
    ON t1.sk_imovel = t3.sk_imovel
GROUP BY t3.tipo_propriedade,t2.bairro