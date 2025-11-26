-- Crie um relatório que exiba o número total de reservas com os bairros nas linhas e os meses do ano nas colunas

SELECT 
    t2.bairro,
    COUNT(*) FILTER (WHERE t3.mes = 1) AS jan,
    COUNT(*) FILTER (WHERE t3.mes = 2) AS fev,
    COUNT(*) FILTER (WHERE t3.mes = 3) AS mar,
    COUNT(*) FILTER (WHERE t3.mes = 4) AS abr,
    COUNT(*) FILTER (WHERE t3.mes = 5) AS mai,
    COUNT(*) FILTER (WHERE t3.mes = 6) AS jun,
    COUNT(*) FILTER (WHERE t3.mes = 7) AS jul,
    COUNT(*) FILTER (WHERE t3.mes = 8) AS ago,
    COUNT(*) FILTER (WHERE t3.mes = 9) AS set,
    COUNT(*) FILTER (WHERE t3.mes = 10) AS out,
    COUNT(*) FILTER (WHERE t3.mes = 11) AS nov,
    COUNT(*) FILTER (WHERE t3.mes = 12) AS dez,
    COUNT(*) as total_ano
FROM 
    fato_reservas t1
JOIN dim_localizacao t2 
    ON t1.sk_localizacao = t2.sk_localizacao
JOIN dim_data t3
    ON t1.sk_data = t3.sk_data
GROUP BY t2.bairro
ORDER BY t2.bairro;
