"""
Простая модель классификации ирисов без scikit-learn
"""
import math

# Данные ирисов Фишера (встроенные в код)
IRIS_DATA = [
    # setosa (класс 0)
    [5.1, 3.5, 1.4, 0.2, 0], [4.9, 3.0, 1.4, 0.2, 0], [4.7, 3.2, 1.3, 0.2, 0],
    # versicolor (класс 1)  
    [7.0, 3.2, 4.7, 1.4, 1], [6.4, 3.2, 4.5, 1.5, 1], [6.9, 3.1, 4.9, 1.5, 1],
    # virginica (класс 2)
    [6.3, 3.3, 6.0, 2.5, 2], [5.8, 2.7, 5.1, 1.9, 2], [7.1, 3.0, 5.9, 2.1, 2]
]

CLASS_NAMES = ['setosa', 'versicolor', 'virginica']

def predict_iris(sepal_length, sepal_width, petal_length, petal_width):
    """Простой классификатор по ближайшему соседу"""
    input_point = [sepal_length, sepal_width, petal_length, petal_width]
    
    # Находим ближайшую точку в данных
    min_distance = float('inf')
    best_class = 0
    
    for data_point in IRIS_DATA:
        # Считаем евклидово расстояние
        distance = 0
        for i in range(4):
            distance += (input_point[i] - data_point[i]) ** 2
        distance = math.sqrt(distance)
        
        if distance < min_distance:
            min_distance = distance
            best_class = data_point[4]
    
    return CLASS_NAMES[best_class]

# Тестируем
if __name__ == "__main__":
    result = predict_iris(5.1, 3.5, 1.4, 0.2)
    print(f"Тестовое предсказание: {result}")