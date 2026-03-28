#ifndef RUN_H
#define RUN_H

#include <memory>
#include "engines.h"

class App {
private:
    std::unique_ptr<AEngine> engine;  // Просто объявление

public:
    App();  // Конструктор
    void run();
};

#endif // RUN_H