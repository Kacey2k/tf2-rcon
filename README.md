# TF2 RCON

A minimal Python command-line program for sending RCON (Remote Console) commands to your local Team Fortress 2 client.

This serves as a foundation for interfacing with the TF2 client using console commands, which can be adapted to support infinite automative/utility projects that interact with TF2.

This same approach can be adapted for other Valve Source-1 games as well, just with a slightly different setup.

## Usage

1. Add "-usercon" to your TF2 launch options.
2. Add the following lines to your autoexec.cfg file. Located at: ``...\Steam\steamapps\common\Team Fortress 2\tf\cfg``
```cfg
ip 0.0.0.0
hostport 27015
rcon_password "choose_your_own_password"
net_start
```
Make sure the password you set is updated in the Python program as well. (And port if you change that).

3. Open TF2.
4. Run the program; if you set it up correctly, it will accept input as individual Rcon commands.

```bash
python tf2_rcon.py
```

Enter `exit` to disconnect.

## Notes

- Intended as a small educational proof of concept, designed to be implemented in larger projects that interface with TF2 via Rcon.
- Remember to keep your RCON password private and do not commit it publicly.
- If you use Mastercomfig, ensure you add the required lines in Step 2 to: ``\Team Fortress 2\tf\cfg\overrides\autoexec.cfg``
- For some commands (like `echo`), if you prepend them with a `wait` command, the execution context changes so that the return value is sent to the in-game console (and thus the `console.log` if you need text sent there) as opposed to the program's terminal. Example: `wait 33; echo "Hello, world!"`

## Troubleshooting

### Connection Refused / Timed Out
- Make sure TF2 is running when you start the program.
- Make sure TF2 has been restarted if you added `-usercon` or updated your autoexec.cfg file.
- Make sure another program is not using the same port. (You can change it if needed)

### Authentication Failed
- The password in the Python program must match the one set in the autoexec.cfg EXACTLY.

### The Config did not load
- Verify you created the file in ``/tf/cfg/autoexec.cfg`` or in ``/tf/cfg/overrides/autoexec.cfg`` if you actively use Mastercomfig.
- Verify Windows did not save it as "autoexec.cfg.txt"

### Connected, but a Command Returned Nothing
An empty response does not always mean the command failed. Some commands simply return no response even though they were executed.

To verify responses are being received properly, test with:
```python
echo "Hello, World!"
```
The echo command returns the text to the program when executed.

### The Connection Suddenly Closed
TF2 can close the connection when:
- The game closes
- The RCON configuration is updated
- The network system is restarted
- The PC enters sleep

This program is intentionally simple and does not reconnect automatically. 
Close it, make sure TF2 is running, and start it again.

## Credits / Reference

https://developer.valvesoftware.com/wiki/Source_RCON_Protocol - Source RCON Documentation.

https://docs.python.org/3/library/socket.html - Python's Socket Module

https://docs.python.org/3/library/struct.html - Python's Struct Module
