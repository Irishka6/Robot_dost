#include "../include/run.h"
#include "../include/engines.h"
#include "../include/fooengines.h"
#include <memory>

App::App() : engine(new FooEngine()) {
}

void App::run() {
    engine->forward(1000);
}