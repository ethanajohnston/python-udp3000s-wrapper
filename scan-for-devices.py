
##### Use this to read if devices are connected and to get  #####
import pyvisa

def list_visa_devices_with_id():
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()

    if not resources:
        print("No VISA devices found.")
        return

    print("Connected VISA devices:\n")
    for rname in resources:
        print(f"Resource: {rname}")
        try:
            inst = rm.open_resource(rname)
            inst.timeout = 2000  # 2s timeout
            inst.read_termination = '\n'
            inst.write_termination = '\n'
            try:
                idn = inst.query("*IDN?")
                print(f"  *IDN?: {idn.strip()}")
            except Exception as e:
                print(f"  Could not query *IDN?: {e}")
            inst.close()
        except Exception as e:
            print(f"  Could not open: {e}")
        print()

if __name__ == "__main__":
    list_visa_devices_with_id()
