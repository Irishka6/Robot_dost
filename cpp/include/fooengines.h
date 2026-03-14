#include "engines.h"
#include <string>

class FooEngine : public AEngine {
private:
    bool is_moving;
    int current_speed;
    std::string engine_type;

public:
    // Конструктор и деструктор
    FooEngine();
    ~FooEngine() override;

    // Переопределение виртуальных методов базового класса
    void forward(int time_ms) override;
    void right(int time_ms) override;
    void left(int time_ms) override;
    void stop() override;
}