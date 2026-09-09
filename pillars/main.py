def run(num_pillars: int, gap_pillars: float, pillar_width: float) -> float:
    if num_pillars <= 1:
        return 0.0

    # Convertimos la distancia del hueco de metros a centímetros
    gap_cm = gap_pillars * 100

    # Distancia de bordes internos: (N - 1) huecos + (N - 2) pilares intermedios
    inter_distance = (num_pillars - 1) * gap_cm + (num_pillars - 2) * pillar_width

    return float(inter_distance)


if __name__ == '__main__':
    # Valores de ejemplo del ejercicio
    num_pillars = 5
    gap_pillars = 2.25  # metros
    pillar_width = 75   # cm

    # Ejecutamos la función directamente
    resultado = run(num_pillars, gap_pillars, pillar_width)
    
    print(f"Resultado final: {resultado} cm")