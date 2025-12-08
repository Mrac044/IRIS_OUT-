"""
Простая модель классификации ирисов без scikit-learn
"""
IRIS_DATA = [
    [5.1, 3.5, 1.4, 0.2, 0], [4.9, 3.0, 1.4, 0.2, 0],
    [7.0, 3.2, 4.7, 1.4, 1], [6.4, 3.2, 4.5, 1.5, 1],
    [6.3, 3.3, 6.0, 2.5, 2], [5.8, 2.7, 5.1, 1.9, 2]
]
CLASS_NAMES = ['setosa', 'versicolor', 'virginica']

def predict_iris(sepal_length, sepal_width, petal_length, petal_width):
    """Простой классификатор по ближайшему соседу"""
    input_point = [sepal_length, sepal_width, petal_length, petal_width]
    min_distance = float('inf')
    best_class = 0
    
    for data_point in IRIS_DATA:
        distance = sum((a - b) ** 2 for a, b in zip(input_point, data_point[:4]))
        if distance < min_distance:
            min_distance = distance
            best_class = data_point[4]
    
    return CLASS_NAMES[best_class]

    # fuck my developing life >:(