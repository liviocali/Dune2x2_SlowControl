# Slow Control scipts for the DUNE ND-LAr 2x2 demonstrator

## Configuration
Configuration filename by default: "config.ini"\
To use example config file:\
`cp config_example.ini config.ini`

## Start scripts on device
Each directory (e.g. `RTD, PFD5,..`) contains two executable bash scripts:
- `start_<DEVICE>.sh` to start the readout in the current session (for debugging)
- `start_<DEVICE>_in_screen.sh` to start the readout in a detached screen session in the background

## Start scripts from remote
TO BE ADDED


## Task List
- [ ] Check Spellman scripts, update to InfluxDB v2 and implement config parser
- [ ] Write MPOD scripts
- [ ] Update RTD scripts to include module number
- [ ] Write general example script of how to push to InfluxDB2
- [ ] Setup Grafana pages
- [ ] Upload/Write remote start/stop scripts
- [ ] Have a beer :beer:
