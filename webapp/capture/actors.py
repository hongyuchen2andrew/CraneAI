from webapp import dramatiq


@dramatiq.actor
def cop():
    print("Cop actor")
    with open("/tmp/cop.txt", "w") as f:
        f.write("Cop actor")
    return "Cop actor"
