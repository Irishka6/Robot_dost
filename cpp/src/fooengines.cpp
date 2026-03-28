#include "../include/fooengines.h"
#include <iostream>
#include <chrono>
#include <thread>

// Реализация конструктора
FooEngine::FooEngine() : is_moving(false), current_speed(0), engine_type("FooEngine v1.0") {
    std::cout << "FooEngine initialized: " << engine_type << std::endl;
}

// Реализация деструктора
FooEngine::~FooEngine() {
    stop();
    std::cout << "FooEngine shutting down" << std::endl;
}

void FooEngine::forward(int time_ms) {
    std::cout << "FooEngine forward " << time_ms << "ms" << std::endl;
    stop();
}

void FooEngine::right(int time_ms) {
    std::cout << "FooEngine right " << time_ms << "ms" << std::endl;
    is_moving = true;
    current_speed = 50;
    std::this_thread::sleep_for(std::chrono::milliseconds(time_ms));
    stop();
}

void FooEngine::left(int time_ms) {
    std::cout << "FooEngine left " << time_ms << "ms" << std::endl;
    is_moving = true;
    current_speed = 50;
    std::this_thread::sleep_for(std::chrono::milliseconds(time_ms));
    stop();
}

void FooEngine::stop() {
    if (is_moving) {
        std::cout << "FooEngine stopping..." << std::endl;
        is_moving = false;
        current_speed = 0;
    }
}

// Дополнительные методы, если они объявлены в заголовке
int FooEngine::getCurrentSpeed() const {
    return current_speed;
}

bool FooEngine::isMoving() const {
    return is_moving;
}

std::string FooEngine::getEngineType() const {
    return engine_type;
}

void FooEngine::calibrate() {
    std::cout << "FooEngine calibrating..." << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    std::cout << "FooEngine calibration complete" << std::endl;
}