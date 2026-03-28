#ifndef ENGINES_H
#define ENGINES_H
// Ѕазовый абстрактный класс дл€ разных типов роботов
class AEngine {
public:
    // ¬иртуальный деструктор дл€ правильного удалени€ через указатель на базовый класс
    virtual ~AEngine() = default;

    virtual void forward(int time_ms) = 0;

    virtual void right(int time_ms) = 0;
    
    virtual void left(int time_ms) = 0;
    
    virtual void stop() = 0;
};
#endif // ENGINES_H

    