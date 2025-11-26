-- Número de imóveis alugados apenas no bairro 'Tijuca’ ou 'Leblon' (slice), comparando meses do ano (dice).

SELECT 
    t2.bairro,
    t3.mes,
    COUNT(*) AS quantidade_reservas
FROM fato_reservas t1
JOIN dim_localizacao t2 
    ON t1.sk_localizacao = t2.sk_localizacao
JOIN dim_data t3
    ON t1.sk_data = t3.sk_data
WHERE t2.bairro IN ('Tijuca', 'Leblon')
GROUP BY t3.mes,t2.bairro             
ORDER BY t2.bairro,t3.mes;


