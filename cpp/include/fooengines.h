#ifndef FOOENGINES_H
#define FOOENGINES_H

#include "engines.h"
#include <string>

class FooEngine : public AEngine {
private:
    bool is_moving;
    int current_speed;
    std::string engine_type;

public: 
    FooEngine();  // конструктор
    ~FooEngine() override;  // деструктор
    
    void forward(int time_ms) override;
    void right(int time_ms) override;
    void left(int time_ms) override;
    void stop() override;
    
    // ƒополнительные методы
    int getCurrentSpeed() const;
    bool isMoving() const;
    std::string getEngineType() const;
    void calibrate();
};

#endif // FOOENGINES_H