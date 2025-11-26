-- Qual o faturamento total com aluguéis em um bairro, agregado por mês e, em seguida, por trimestre

SELECT 
    t2.bairro,
    t3.mes,
    t3.trimestre,
    COUNT(*) AS quantidade_imoveis,
    SUM(t1.preco) AS faturamento_mensal,
    SUM(SUM(t1.preco)) OVER (
        PARTITION BY t2.bairro, t3.trimestre
    ) AS faturamento_trimestral
FROM
    fato_reservas t1
JOIN dim_localizacao t2
    ON t1.sk_localizacao = t2.sk_localizacao
JOIN dim_data t3
    ON t1.sk_data = t3.sk_data
GROUP BY 
    t2.bairro, t3.mes, t3.trimestre
ORDER BY
    t2.bairro, t3.mes;
