# Robot_dost
## **README.md — Архитектура системы (Python + C++)**

# Система доставки с управлением жестами
## Гибридная архитектура: Python (OpenCV) + C++ (управление роботом)

## Обзор

Документ описывает архитектуру системы, где:
- **Python + OpenCV** — распознавание жестов и API
- **C++** — управление роботом (производительность, аппаратный контроль)
- **CTypes/PyBind11** — связь между Python и C++

---

## Структура проекта

```
gesture_delivery_system/
?
??? README.md                          # Документация
??? requirements.txt                    # Python зависимости
??? CMakeLists.txt                      # Сборка C++ кода
??? .env.example                        # Шаблон конфигурации
?
??? src/
?   ??? python/                         # Python модули
?   ?   ??? main.py                      # Точка входа
?   ?   ?
?   ?   ??? api/                         # REST API
?   ?   ?   ??? server.py                 # Flask/FastAPI сервер
?   ?   ?   ??? routes.py                 # Эндпоинты
?   ?   ?
?   ?   ??? video/                        # Обработка видео (OpenCV)
?   ?   ?   ??? camera.py                  # Управление камерой
?   ?   ?   ??? video_processor.py         # Обработка видеопотока
?   ?   ?   ??? gesture_recognizer.py      # Распознавание жестов
?   ?   ?
?   ?   ??? server/                        # Серверная логика
?   ?   ?   ??? main_server.py              # Основной сервер
?   ?   ?   ??? route_planner.py            # Планирование маршрута
?   ?   ?   ??? command_generator.py        # Генерация команд
?   ?   ?
?   ?   ??? models/                         # Модели данных
?   ?   ?   ??? student.py
?   ?   ?   ??? robot.py
?   ?   ?   ??? order.py
?   ?   ?   ??? coordinates.py
?   ?   ?   ??? gesture.py
?   ?   ?
?   ?   ??? robot/                          # Связь с C++
?   ?   ?   ??? robot_controller_wrapper.py  # CTypes обертка
?   ?   ?   ??? robot_interface.py           # Абстрактный интерфейс
?   ?   ?
?   ?   ??? utils/                           # Утилиты
?   ?       ??? logger.py
?   ?       ??? config.py
?   ?
?   ??? cpp/                               # C++ код
?       ??? include/
?       ?   ??? robot_controller.h          # Основной контроллер
?       ?   ??? motion_control.h             # Управление движением
?       ?   ??? robot_hardware.h             # Аппаратный уровень
?       ?   ??? robot_types.h                # Структуры и enum
?       ?
?       ??? src/
?       ?   ??? robot_controller.cpp
?       ?   ??? motion_control.cpp
?       ?   ??? robot_hardware.cpp
?       ?
?       ??? bindings/                        # Связка с Python
?           ??? pybind11_bindings.cpp        # Для PyBind11
?           ??? ctypes_wrapper.cpp            # Для CTypes
?
??? build/                                 # Директория сборки
??? models/                                # Обученные модели
?   ??? gesture_model.pb
?
??? docs/                                   # Документация
    ??? api_documentation.md
    ??? class_diagram.puml
```

---

## Компоненты системы

### 1. Python-часть (Высокоуровневая логика)

#### 1.1 Модуль видеообработки (`video/`)

| Компонент | Назначение | Ключевые методы |
|-----------|------------|-----------------|
| **Camera** | Управление камерой | `start_stream()`, `get_frame()`, `set_resolution()` |
| **VideoProcessor** | Обработка видеопотока | `process_frame()`, `locate_student()`, `locate_robot()` |
| **GestureRecognizer** | Распознавание жестов (OpenCV) | `recognize()`, `get_gesture_type()`, `load_model()` |

**Взаимодействие:** Camera ? VideoProcessor ? GestureRecognizer

---

#### 1.2 Серверный модуль (`server/`)

| Компонент | Назначение | Ключевые методы |
|-----------|------------|-----------------|
| **Server** | Основной координатор | `process_video_stream()`, `build_route()`, `send_command()` |
| **RoutePlanner** | Планирование маршрута | `build_route()`, `optimize_route()`, `add_obstacle()` |
| **CommandGenerator** | Генерация команд | `determine_action_types()`, `build_command()` |

**Взаимодействие:** Server ? RoutePlanner ? CommandGenerator

---

#### 1.3 API модуль (`api/`)

| Компонент | Назначение | Эндпоинты |
|-----------|------------|-----------|
| **APIServer** | REST API интерфейс | `GET /status`, `POST /orders`, `GET /robots/{id}` |

---

#### 1.4 Модели данных (`models/`)

| Класс | Атрибуты | Методы |
|-------|----------|--------|
| **Student** | `id`, `name`, `location`, `status` | `submit_gesture()`, `confirm_delivery()` |
| **Robot** | `id`, `location`, `battery`, `status` | `accept_command()`, `move_to()`, `send_report()` |
| **Order** | `id`, `student_id`, `robot_id`, `gesture`, `status` | `update_status()`, `assign_robot()` |
| **Coordinates** | `x`, `y`, `z` | `distance_to()`, `add()`, `subtract()` |
| **Gesture** | `id`, `type`, `confidence`, `timestamp` | `to_json()`, `get_type()` |

---

#### 1.5 Модуль связи с C++ (`robot/`)

| Компонент | Назначение | Методы |
|-----------|------------|--------|
| **RobotInterface** | Абстрактный интерфейс робота | `connect()`, `move_to()`, `get_status()` |
| **RobotControllerWrapper** | CTypes обертка для C++ | Вызов C++ функций через `ctypes` |

---

### 2. C++-часть (Низкоуровневое управление)

#### 2.1 Основные компоненты

| Компонент | Назначение | Ключевые методы |
|-----------|------------|-----------------|
| **RobotController** | Главный контроллер | `accept_command()`, `execute_action()`, `generate_report()` |
| **MotionController** | Управление движением | `move_forward()`, `rotate_to()`, `calibrate()` |
| **RobotHardware** | Аппаратный уровень | `set_motor_speed()`, `read_encoder()`, `read_battery()` |

**Взаимодействие:** RobotController ? MotionController ? RobotHardware

---

#### 2.2 Структуры данных (`robot_types.h`)

```cpp
struct Coordinates { double x, y, z; };
enum class RobotStatus { IDLE, MOVING, ROTATING, PICKING_UP, DELIVERING, ERROR };
enum class ActionType { MOVE_FORWARD, ROTATE, STOP, PICK_UP, DELIVER };
struct RobotCommand { string id; vector<ActionType> actions; vector<double> params; };
struct DeliveryReport { string id; string order_id; vector<Coordinates> route; };
```

---

### 3. Связь Python и C++

#### Вариант A: CTypes (проще)

**C++ экспорт:**
```cpp
extern "C" {
    RobotController* robot_new();
    bool robot_move_to(RobotController* ctrl, double x, double y);
    void robot_delete(RobotController* ctrl);
}
```

**Python вызов:**
```python
lib = ctypes.CDLL("librobot.so")
ctrl = lib.robot_new()
lib.robot_move_to(ctrl, 10.0, 5.0)
```

#### Вариант B: PyBind11 (современнее)

**C++ биндинг:**
```cpp
PYBIND11_MODULE(robot, m) {
    py::class_<RobotController>(m, "RobotController")
        .def(py::init<>())
        .def("move_to", &RobotController::move_to);
}
```

**Python импорт:**
```python
import robot
ctrl = robot.RobotController()
ctrl.move_to(10.0, 5.0)
```

---

## Поток данных

```
[Камера] ? VideoFrame ? [VideoProcessor] ? GestureData ? [Server]
                                                               ?
[Server] ? Coordinates ? [RoutePlanner] ? [CommandGenerator] ??
    ?
[RobotController (C++)] ? RobotCommand
    ?
[MotionController] ? [RobotHardware] ? Физическое движение
    ?
[DeliveryReport] ? [Server] (обратная связь)
```

---

## Use Case ? Классы (маппинг)

| Use Case | Основной класс | Вспомогательные классы |
|----------|----------------|------------------------|
| Подать жестовую команду | `Student` | `Gesture` |
| Трансляция видеопотока | `Camera` | - |
| Обработка видеопотока | `VideoProcessor` | `GestureRecognizer` |
| Определение местоположения | `VideoProcessor` | `Coordinates` |
| Построение маршрута | `RoutePlanner` | `Coordinates`, `Route` |
| Передача команды роботу | `CommandGenerator` | `RobotCommand` |
| Прием команды | `RobotController` (C++) | `RobotCommand` |
| Перемещение к точке выдачи | `MotionController` (C++) | `Coordinates` |
| Получение заказа | `RobotController` (C++) | - |
| Перемещение к студенту | `MotionController` (C++) | `Coordinates` |
| Завершение доставки | `RobotController` (C++) | `DeliveryReport` |
| Подтверждение получения | `Student` | `Confirmation`, `Order` |

---

## Файлы конфигурации

### `.env.example`
```env
# Камера
CAMERA_ID=0
CAMERA_RESOLUTION=640x480

# Модели
MODEL_PATH=./models/gesture_model.pb

# Робот
ROBOT_PORT=/dev/ttyUSB0
ROBOT_LIB_PATH=./build/librobot_ctypes.so
USE_PYBIND11=False

# API
API_HOST=0.0.0.0
API_PORT=5000
```

### `requirements.txt`
```
opencv-python
mediapipe
numpy
flask
flask-cors
python-dotenv
pybind11
```

### `CMakeLists.txt` (основные цели)
- Библиотека `robot_controller` (C++)
- Биндинги для PyBind11 (опционально)
- Обертка для CTypes
- Тесты

---

## Сборка и запуск (концептуально)

```bash
# 1. Сборка C++ части
mkdir build && cd build
cmake ..
make

# 2. Установка Python зависимостей
pip install -r requirements.txt

# 3. Запуск системы
python src/python/main.py
```

---

## Заключение

Данная архитектура обеспечивает:
- **Производительность** C++ для управления роботом
- **Гибкость** Python для компьютерного зрения
- **Четкое разделение** ответственности
- **Масштабируемость** через REST API
- **Два варианта связи** (CTypes для простоты, PyBind11 для удобства)
