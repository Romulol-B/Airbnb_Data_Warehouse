--Qual o preço médio da diária para casas/apartamentos (slice) com mais de dois quartos (dice)

SELECT
    *
FROM
    fato_reservas t1
JOIN dim_imoveis t2
    ON t1.sk_imovel = t2.sk_imovel

WHERE t2.tipo_quarto = 'Entire home/apt' AND t2.nro_quartos >= 2

