"""
Р—Р°РїСѓСЃРєР°С‚СЊ Р­РўРћРў С„Р°Р№Р» РЅР° СЂРѕР±РѕС‚Рµ РґР»СЏ РїСЂРёРµРјР° РєРѕРјР°РЅРґ
РџРѕРґРґРµСЂР¶РёРІР°РµС‚ Рё REST, Рё MQTT
"""


# ============= REST РЎР•Р Р’Р•Р  Р”Р›РЇ Р РћР‘РћРўРђ =============
def run_rest_server(host="0.0.0.0", port=8000):
    """Р—Р°РїСѓСЃРє REST СЃРµСЂРІРµСЂР° РЅР° СЂРѕР±РѕС‚Рµ"""
    try:
        from fastapi import FastAPI, HTTPException
        from pydantic import BaseModel
        import uvicorn

        app = FastAPI(title="Robot Control API")

        class RobotCommand(BaseModel):
            comman: str
            id: int
            time: float = 1.0

        # Р¤СѓРЅРєС†РёРё СѓРїСЂР°РІР»РµРЅРёСЏ СЂРѕР±РѕС‚РѕРј (Р·Р°РјРµРЅРёС‚Рµ РЅР° СЂРµР°Р»СЊРЅС‹Рµ)
        def move_forward(duration):
            print(f"[ROBOT] Moving FORWARD for {duration} seconds")
            # Р—РґРµСЃСЊ РєРѕРґ СѓРїСЂР°РІР»РµРЅРёСЏ РјРѕС‚РѕСЂР°РјРё

        def move_backward(duration):
            print(f"[ROBOT] Moving BACKWARD for {duration} seconds")

        def turn_left():
            print(f"[ROBOT] Turning LEFT")

        def turn_right():
            print(f"[ROBOT] Turning RIGHT")

        def stop():
            print(f"[ROBOT] STOP")

        @app.post("/commands")
        @app.post("/api/command")
        async def execute_command(command: RobotCommand):
            print(f"[ROBOT] Command received: {command.comman} (id={command.id}, time={command.time})")

            if command.comman == "forward":
                move_forward(command.time)
            elif command.comman == "backward":
                move_backward(command.time)
            elif command.comman == "left":
                turn_left()
            elif command.comman == "right":
                turn_right()
            elif command.comman == "stop":
                stop()
            else:
                raise HTTPException(status_code=400, detail=f"Unknown command: {command.comman}")

            return {"status": "ok", "executed": command.comman}

        @app.get("/status")
        async def get_status():
            return {"status": "online", "battery": 100}

        print(f"[ROBOT] REST server starting on http://{host}:{port}")
        uvicorn.run(app, host=host, port=port)

    except ImportError:
        print("FastAPI not installed. Run: pip install fastapi uvicorn pydantic")


# ============= MQTT РљР›Р�Р•РќРў Р”Р›РЇ Р РћР‘РћРўРђ =============
def run_mqtt_receiver(broker_host="localhost", broker_port=1883, topic="robot/commands"):
    """Р—Р°РїСѓСЃРє MQTT РїСЂРёРµРјРЅРёРєР° РЅР° СЂРѕР±РѕС‚Рµ"""
    import paho.mqtt.client as mqtt
    import json

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"[ROBOT] Connected to MQTT broker at {broker_host}:{broker_port}")
            client.subscribe(topic)
            print(f"[ROBOT] Subscribed to topic: {topic}")
        else:
            print(f"[ROBOT] Failed to connect, error code: {rc}")

    def on_message(client, userdata, msg):
        try:
            payload = msg.payload.decode('utf-8')
            print(f"[ROBOT] Command received: {payload}")
            command = json.loads(payload)

            # Р’С‹РїРѕР»РЅРµРЅРёРµ РєРѕРјР°РЅРґС‹
            cmd = command.get('comman')
            print(f"[ROBOT] Executing: {cmd}")
            # Р—РґРµСЃСЊ РєРѕРґ СѓРїСЂР°РІР»РµРЅРёСЏ СЂРѕР±РѕС‚РѕРј

        except Exception as e:
            print(f"[ROBOT] Error processing message: {e}")

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(broker_host, broker_port, 60)
        client.loop_forever()
    except Exception as e:
        print(f"[ROBOT] MQTT error: {e}")


# ============= Р—РђРџРЈРЎРљ =============
if __name__ == "__main__":
    import sys

    print("Robot Receiver Starting...")
    print("Options:")
    print("  1 - REST server (port 8000)")
    print("  2 - MQTT client")

    choice = input("Choose mode (1 or 2): ").strip()

    if choice == "1":
        run_rest_server()
    elif choice == "2":
        host = input("MQTT broker IP (default localhost): ").strip() or "localhost"
        run_mqtt_receiver(broker_host=host)
    else:
        print("Invalid choice")