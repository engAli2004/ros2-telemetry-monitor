import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/naserddinee0/telemetry_ws/install/robot_health_monitor'
