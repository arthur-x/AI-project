#ifndef _FLIGHTGEAR_DATA_H_
#define _FLIGHTGEAR_DATA_H_

#define MAX_ENGINES 12
#define MAX_TANKS 8
#define MAX_BOOSTPUMPS 2
#define MAX_WHEELS 3
#define MAX_HYD_SYSTEMS 4
#define MAX_PACKS 4
#define MAX_STATIONS 12
#define MAX_EJECTION_SEATS 10
#define MAX_AUTOPILOTS 3

#define FD_clock "clock-indicated"
#define FD_aileron "aileron"
#define FD_elevator "elevator"
#define FD_rudder "rudder"
#define FD_throttle0 "throttle0"
#define FD_throttle1 "throttle1"
#define FD_vsi_fpm "vsi-fpm"
#define FD_alt_ft "alt-ft"
#define FD_ai_pitch "ai-pitch"
#define FD_ai_roll "ai-roll"
#define FD_ai_offset "ai-offset"
#define FD_hi_heading "hi-heading"

#define FD_roll_deg "roll-deg"
#define FD_pitch_deg "pitch-deg"
#define FD_heading_deg "heading-deg"

#define FD_airspeed "airspeed-kt"
#define FD_speed_north_fps "speed-north-fps"
#define FD_speed_east_fps "speed-east-fps"
#define FD_speed_down_fps "speed-down-fps"
#define FD_uBody_fps "uBody-fps"
#define FD_vBody_fps "vBody-fps"
#define FD_wBody_fps "wBody-fps"


#define FD_north_accel_fps_sec "north-accel-fps_sec"
#define FD_east_accel_fps_sec "east-accel-fps_sec"
#define FD_down_accel_fps_sec "down-accel-fps_sec"
#define FD_x_accel_fps_sec "x-accel-fps_sec"
#define FD_y_accel_fps_sec "y-accel-fps_sec"
#define FD_z_accel_fps_sec "z-accel-fps_sec"

#define FD_latitude "latitude"
#define FD_longitude "longitude"
#define FD_altitude "altitude"



#define TAKE_OFF_MODE 0
#define NORMAL_FLY_MODE 1
#define TOUCH_DOWN_MODE 2

struct FGInstrumentation
{
	double vsi_fpm;
    double alt_ft;
    double ai_pitch;
    double ai_roll;
    double ai_offset;
    double hi_heading;

};

struct FGOrientation
{
	double roll;
    double pitch;
    double heading;
};

struct FGVelocities
{
	double airspeed;
	double speed_north;
    double speed_east;
    double speed_down;

	double uBody;
	double vBody;
	double wBody;

};

struct FGAccelerations
{
	double north_accel_fps_sec;
    double east_accel_fps_sec;
    double down_accel_fps_sec;

	double x_accel_fps_sec;
	double y_accel_fps_sec;
	double z_accel_fps_sec;

};

struct FGPosition
{
	double latitude;
    double longitude;
    double altitude;
};

struct FGControls
{
	char clock[30];
    double aileron;
    double elevator;
    double rudder;
    double throttle[2];
	


/*
    // controls/flight/
    double aileron;
    double aileron_trim;
    double elevator;
    double elevator_trim;
    double rudder;
    double rudder_trim;
    double flaps;
    double slats;
    bool BLC;          // Boundary Layer Control
    double spoilers;
    double speedbrake;
    double wing_sweep;
    bool wing_fold;
    bool drag_chute;

    // controls/engines/
    bool throttle_idle;

    // controls/engines/engine[n]/
    double throttle[MAX_ENGINES];
    bool starter[MAX_ENGINES];
    bool fuel_pump[MAX_ENGINES];
    bool fire_switch[MAX_ENGINES];
    bool fire_bottle_discharge[MAX_ENGINES];
    bool cutoff[MAX_ENGINES];
    double mixture[MAX_ENGINES];
    double prop_advance[MAX_ENGINES];
    int magnetos[MAX_ENGINES];
    int feed_tank[MAX_ENGINES];
    bool nitrous_injection[MAX_ENGINES];  // War Emergency Power
    double cowl_flaps_norm[MAX_ENGINES];
    bool feather[MAX_ENGINES];
    int ignition[MAX_ENGINES];
    bool augmentation[MAX_ENGINES];
    bool reverser[MAX_ENGINES];
    bool water_injection[MAX_ENGINES];
    double condition[MAX_ENGINES];           // turboprop speed select

    // controls/fuel/
    bool dump_valve;

    // controls/fuel/tank[n]/
    bool fuel_selector[MAX_TANKS];
    int to_engine[MAX_TANKS];
    int to_tank[MAX_TANKS];
    
    // controls/fuel/tank[n]/pump[p]/
    bool boost_pump[MAX_TANKS * MAX_BOOSTPUMPS];

    // controls/gear/
    double brake_left;
    double brake_right;
    double copilot_brake_left;
    double copilot_brake_right;
    double brake_parking;
    double steering;
    bool nose_wheel_steering;
    bool gear_down;
    bool antiskid;
    bool tailhook;
    bool launchbar;
    bool catapult_launch_cmd;
    bool tailwheel_lock;

    // controls/gear/wheel[n]/
    bool alternate_extension[MAX_WHEELS];

    // controls/anti-ice/
    bool wing_heat;
    bool pitot_heat;
    int wiper;
    bool window_heat;

    // controls/anti-ice/engine[n]/
    bool carb_heat[MAX_ENGINES];
    bool inlet_heat[MAX_ENGINES];
    
    // controls/hydraulic/system[n]/
    bool engine_pump[MAX_HYD_SYSTEMS];
    bool electric_pump[MAX_HYD_SYSTEMS];

    // controls/electric/
    bool battery_switch;
    bool external_power;
    bool APU_generator;

    // controls/electric/engine[n]/
    bool generator_breaker[MAX_ENGINES];
    bool bus_tie[MAX_ENGINES];

    // controls/pneumatic/
    bool APU_bleed;

    // controls/pneumatic/engine[n]/
    bool engine_bleed[MAX_ENGINES];
    
    // controls/pressurization/
    int mode;
    bool dump;
    double outflow_valve;

    // controls/pressurization/pack[n]/
    bool pack_on[MAX_PACKS];

    // controls/lighting/
    bool landing_lights;
    bool turn_off_lights;
    bool taxi_light;
    bool logo_lights;
    bool nav_lights;
    bool beacon;
    bool strobe;
    double panel_norm;
    double instruments_norm;
    double dome_norm;

    // controls/armament/
    bool master_arm;
    int station_select;
    bool release_ALL;

    // controls/armament/station[n]/
    int stick_size[MAX_STATIONS];
    bool release_stick[MAX_STATIONS];
    bool release_all[MAX_STATIONS];
    bool jettison_all[MAX_STATIONS];

    // controls/seat/
    double vertical_adjust;
    double fore_aft_adjust;
    bool eject[MAX_EJECTION_SEATS];
    int eseat_status[MAX_EJECTION_SEATS];
    int cmd_selector_valve;

    // controls/APU/
    int off_start_run;
    bool APU_fire_switch;

    // controls/autoflight/autopilot[n]/
    bool autopilot_engage[MAX_AUTOPILOTS];

    // controls/autoflight/
    bool autothrottle_arm;
    bool autothrottle_engage;
    double heading_select;
    double altitude_select;
    double bank_angle_select;
    double vertical_speed_select;
    double speed_select;
    double mach_select; 
    int vertical_mode;
    int lateral_mode;
 */    

};

struct FGAlldata
{
	struct FGInstrumentation Instrumentation;
	struct FGOrientation Orientation;
	struct FGVelocities Velocities;
	struct FGAccelerations Accelerations;
	struct FGPosition Position;
	struct FGControls Controls;

};
/*
typedef struct FG_UDP_Parameter
{
	char keyword[30];
	char keyvalue[20];
	struct FG_UDP_Parameter *next;
}Fg_Para;

*/
#endif
