#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <WS2tcpip.h>
#include <WinSock2.h> 
#include <windows.h>
#include "../include/flightgear_data.h"
#include <math.h>
#pragma comment (lib, "ws2_32.lib")     
#define DEFAULT_TEST_WRITE_FILE_PATH "./out.txt"//即时通信模式下用这个文件
#define DEFAULT_TEST_REC_FILE_PATH "./test.txt"//记录模式下用这个文件
#define DEFAULT_TEST_READ_FILE_PATH "./in.txt"
#define roll_adjust_interval 10


struct FGAlldata g_FgData;

HANDLE fg_data_Mutex = NULL;
HANDLE rec_flag_Mutex = NULL;
int rec_flag = 0;//程序流程：读取接受的状态数据，然后发送控制数据，再接受，如此循环...
int fly_mode = 0;
void load_fgdata(char* data)//将data读到全局变量 g_FgData 中
{	
	int i = 0;
	int j = 0;
	char keyword[30]={0};
	char keyvalue[20]={0};
	int valueflag = 0;
	
	WaitForSingleObject( fg_data_Mutex, INFINITE);
	
	while(1)
	{
		if((data[i] != ',')&& (data[i] != 0))
		{	
			if(data[i]=='=')
			{
				valueflag = 1;
				i++;
				j=0;
			}
			if(!valueflag)
				keyword[j++] = data[i++];
			else
				keyvalue[j++] = data[i++];
		}			
		else 
		{
			if(!strcmp(keyword,FD_clock))
			{
				memset(g_FgData.Controls.clock,0,30);
				strcpy(g_FgData.Controls.clock,keyvalue);
			}
			else if(!strcmp(keyword,FD_aileron))
			{
				g_FgData.Controls.aileron = atof(keyvalue);
			}
			else if(!strcmp(keyword,FD_elevator))
			{
				g_FgData.Controls.elevator = atof(keyvalue);
			}
			else if(!strcmp(keyword,FD_rudder))
			{
				g_FgData.Controls.rudder = atof(keyvalue);
			}
			else if(!strcmp(keyword,FD_throttle0))
			{
				g_FgData.Controls.throttle[0] = atof(keyvalue);
			}
			else if(!strcmp(keyword,FD_throttle1))
			{
				g_FgData.Controls.throttle[1] = atof(keyvalue);
			}
			else if(!strcmp(keyword,FD_vsi_fpm))
			{
				g_FgData.Instrumentation.vsi_fpm = atof(keyvalue);
			}
			else if(!strcmp(keyword,FD_alt_ft))
			{
				g_FgData.Instrumentation.alt_ft = atof(keyvalue);
			}
			else if(!strcmp(keyword,FD_ai_pitch))
			{
				g_FgData.Instrumentation.ai_pitch = atof(keyvalue);
			}
			else if(!strcmp(keyword,FD_ai_roll))
			{
				g_FgData.Instrumentation.ai_roll = atof(keyvalue);
			}
			else if(!strcmp(keyword,FD_ai_offset))
			{
				g_FgData.Instrumentation.ai_offset = atof(keyvalue);
			}		
			else if(!strcmp(keyword,FD_hi_heading))
			{
				g_FgData.Instrumentation.hi_heading = atof(keyvalue);
			}
			else if(!strcmp(keyword,FD_roll_deg))
			{
				g_FgData.Orientation.roll = atof(keyvalue);
			}
			else if(!strcmp(keyword,FD_pitch_deg))
			{
				g_FgData.Orientation.pitch = atof(keyvalue);
			}
			else if(!strcmp(keyword,FD_heading_deg))
			{
				g_FgData.Orientation.heading = atof(keyvalue);
			}

			else if (!strcmp(keyword, FD_airspeed))
			{
				g_FgData.Velocities.airspeed = atof(keyvalue);
			}
			else if(!strcmp(keyword,FD_speed_north_fps))
			{
				g_FgData.Velocities.speed_north = atof(keyvalue);
			}
			else if(!strcmp(keyword,FD_speed_east_fps))
			{
				g_FgData.Velocities.speed_east = atof(keyvalue);
			}
			else if(!strcmp(keyword,FD_speed_down_fps))
			{
				g_FgData.Velocities.speed_down = atof(keyvalue);
			}

			else if (!strcmp(keyword, FD_uBody_fps))
			{
				g_FgData.Velocities.uBody = atof(keyvalue);
			}
			else if (!strcmp(keyword, FD_wBody_fps))
			{
				g_FgData.Velocities.wBody = atof(keyvalue);
			}
			else if (!strcmp(keyword, FD_vBody_fps))
			{
				g_FgData.Velocities.vBody = atof(keyvalue);
			}


			
			else if (!strcmp(keyword, FD_x_accel_fps_sec))
			{
				g_FgData.Accelerations.x_accel_fps_sec = atof(keyvalue);
			}
			else if (!strcmp(keyword, FD_y_accel_fps_sec))
			{
				g_FgData.Accelerations.y_accel_fps_sec = atof(keyvalue);
			}
			else if (!strcmp(keyword, FD_z_accel_fps_sec))
			{
				g_FgData.Accelerations.z_accel_fps_sec = atof(keyvalue);
			}


			else if(!strcmp(keyword,FD_north_accel_fps_sec))
			{
				g_FgData.Accelerations.north_accel_fps_sec = atof(keyvalue);
			}
			else if(!strcmp(keyword,FD_east_accel_fps_sec))
			{
				g_FgData.Accelerations.east_accel_fps_sec = atof(keyvalue);
			}
			else if(!strcmp(keyword,FD_down_accel_fps_sec))
			{
				g_FgData.Accelerations.down_accel_fps_sec = atof(keyvalue);
			}
			
			else if(!strcmp(keyword,FD_latitude))
			{
				g_FgData.Position.latitude = atof(keyvalue);
			}
			else if(!strcmp(keyword,FD_longitude))
			{
				g_FgData.Position.longitude = atof(keyvalue);
			}
			else if(!strcmp(keyword,FD_altitude))
			{
				g_FgData.Position.altitude = atof(keyvalue);
			}
			if (data[i] == 0)
				break;
			j=0;
			i++;
			valueflag = 0;
			memset(keyword,0,30);
			memset(keyvalue,0,20);

		}
	}
	ReleaseMutex(fg_data_Mutex);

}


DWORD WINAPI thread_udp_receive(LPVOID lpThreadParameter)
{

	SOCKET slisten = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
	char recdata[2048];
	int ret = 0;
	int nlen = 0;

	struct sockaddr_in remoteddr;
	struct sockaddr_in sin;
	FILE *fp =NULL;
	char file_path[255];
	memset(file_path, 0, 255);
	strcpy(file_path,DEFAULT_TEST_WRITE_FILE_PATH);
	fp = fopen(file_path, "w");
	if(NULL == fp)
	{
		printf("file not exist\n");
		return 0;
	}
	sin.sin_family = AF_INET;
	sin.sin_port = htons(5700);
	sin.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");
	//sin.sin_addr.s_addr = htonl(INADDR_ANY);
	if (bind(slisten, (SOCKADDR*)&sin, sizeof(sin)) == SOCKET_ERROR)
	{
		printf("bind socket error!\n");
		system("pause");
		return 0;
	}

	nlen = sizeof(remoteddr);
	while (1)
	{
		
		ret = recvfrom(slisten, recdata, 2048, 0, (SOCKADDR*)&remoteddr, &nlen);
		if (ret>0)
		{
			recdata[ret] = 0x00;
			printf("%s\n", recdata);
			fseek(fp, 0, SEEK_SET);//在即时通信模式下，文件中只保存当前状态,要连续记录请将此行注释并改变文件名
			ret = fwrite((void*)recdata,strlen(recdata),1,fp);
			load_fgdata(recdata);

			fflush(fp); 
			rec_flag = 1;//一旦一条数据被记录，就会触发控制线程改变控制变量
		}

	}
	fclose(fp);
	closesocket(slisten);
	return 0;

}

DWORD WINAPI thread_procer(LPVOID lpThreadParameter)
{
	SOCKET sClient = socket(AF_INET, SOCK_DGRAM, 0);
	int nlen = 0;
	float in_buf[5];
	char sendData[1024];
	struct sockaddr_in sclient;
	struct FGAlldata data_temp={0};
	struct FGControls sendControlData = {0};
	int sendlen = 0;
	int ret = 0;
	double heading_error = 0;
	
	FILE *fp =NULL;
	
	char file_path[255];
	memset(file_path, 0, 255);
	strcpy(file_path, DEFAULT_TEST_READ_FILE_PATH);
	fp = fopen(file_path, "r");
	if (NULL == fp)
	{
		printf("file not exist\n");
		return 0;
	}

	sclient.sin_family = AF_INET;
	sclient.sin_port = htons(5701); 
	sclient.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");


	while (1)
	{
		if(rec_flag)
		{
			rec_flag = 0;
			
			WaitForSingleObject( fg_data_Mutex, INFINITE);
			memcpy((void*)&data_temp,(void*)&g_FgData,sizeof(struct FGAlldata));
			ReleaseMutex(fg_data_Mutex);
			//以下是被注释掉的Simple控制代码，记录模式下请用Simple控制
			
			switch(fly_mode)
			{
				case TAKE_OFF_MODE:
					memcpy((void*)&sendControlData,(void*)&data_temp.Controls,sizeof(struct FGControls));
					if ((fabs(g_FgData.Velocities.speed_down) < 1)&&(data_temp.Velocities.airspeed < 120))//还在跑道上跑
					{
						if (g_FgData.Velocities.speed_north < -0.0005)
						{
							if (g_FgData.Accelerations.north_accel_fps_sec < 0.0001)
							{
								sendControlData.rudder = data_temp.Controls.rudder - 0.001;
							}

						}
						else if (g_FgData.Velocities.speed_north > 0.0005)
						{
							if (g_FgData.Accelerations.north_accel_fps_sec > -0.0001)
							{
								sendControlData.rudder = data_temp.Controls.rudder + 0.001;
							}
						}

						if (data_temp.Controls.throttle[0]<0.6)
						{
							sendControlData.throttle[0] = data_temp.Controls.throttle[0] + 0.01;
							sendControlData.throttle[1] = data_temp.Controls.throttle[1] + 0.01;
						}
					}
					else
					{
						if (g_FgData.Velocities.speed_north < -0.005)
						{
							if (g_FgData.Accelerations.north_accel_fps_sec < 0.01)
							{

								sendControlData.rudder = data_temp.Controls.rudder - 0.005;

							}

						}
						else if (g_FgData.Velocities.speed_north > 0.005)
						{
							if (g_FgData.Accelerations.north_accel_fps_sec > -0.01)
							{
								sendControlData.rudder = data_temp.Controls.rudder + 0.005;
							}
						}

					}
					if((g_FgData.Velocities.speed_down<-0.1)||(data_temp.Velocities.airspeed > 121))
					{
						if (data_temp.Controls.elevator >-0.1)
						{
							sendControlData.elevator = data_temp.Controls.elevator - 0.001;
							if (data_temp.Controls.throttle[0]<0.6)
							{
								sendControlData.throttle[0] = data_temp.Controls.throttle[0] + 0.01;
								sendControlData.throttle[1] = data_temp.Controls.throttle[1] + 0.01;
							}

						}
						else if ((data_temp.Controls.elevator <=-0.1)&&(data_temp.Controls.elevator >-0.2))
						{
							sendControlData.elevator = data_temp.Controls.elevator - 0.0001;
							if (data_temp.Controls.throttle[0]<0.6)
							{
								sendControlData.throttle[0] = data_temp.Controls.throttle[0] + 0.01;
								sendControlData.throttle[1] = data_temp.Controls.throttle[1] + 0.01;
							}

						}
						if (data_temp.Orientation.roll != 0)
						{
							sendControlData.aileron = -0.1*(data_temp.Orientation.roll);
						}

					}

					if (data_temp.Position.altitude >= 3000)
					{

						fly_mode = NORMAL_FLY_MODE;

					}


					break;

				case NORMAL_FLY_MODE:
					printf("NORMAL_FLY_MODE\n");
					/*
					if (data_temp.Position.altitude > 4800)
					{
						//即时通信模式
						memcpy((void*)&sendControlData, (void*)&data_temp.Controls, sizeof(struct FGControls));
						fseek(fp, 0, SEEK_SET);
						fscanf(fp, "%f,%f,%f,%f,%f", &in_buf[0], &in_buf[1], &in_buf[2], &in_buf[3], &in_buf[4]);
						sendControlData.aileron = in_buf[0];
						sendControlData.elevator = in_buf[1];
						sendControlData.rudder = in_buf[2];
						sendControlData.throttle[0] = in_buf[3];
						sendControlData.throttle[1] = in_buf[4];
						//即时通信模式结束
					}
					else
					{
					*/
						memcpy((void*)&sendControlData, (void*)&data_temp.Controls, sizeof(struct FGControls));

						if (data_temp.Orientation.roll != 0)
						{
							sendControlData.aileron = -0.1*(data_temp.Orientation.roll);
						}

						sendControlData.elevator = (data_temp.Position.altitude - 4333)*0.00015;
						sendControlData.rudder = 0;
						sendControlData.throttle[0] = 0.6;
						sendControlData.throttle[1] = 0.6;
					
					
					break;

			}
			/*
            //即时通信模式
			memcpy((void*)&sendControlData, (void*)&data_temp.Controls, sizeof(struct FGControls));
			fseek(fp, 0, SEEK_SET);
			fscanf(fp, "%f,%f,%f,%f,%f", &in_buf[0], &in_buf[1], &in_buf[2], &in_buf[3], &in_buf[4]); 
			sendControlData.aileron = in_buf[0];
			sendControlData.elevator = in_buf[1];
			sendControlData.rudder = in_buf[2];
			sendControlData.throttle[0] = in_buf[3];
			sendControlData.throttle[1] = in_buf[4];
			//即时通信模式结束
			*/
			sprintf(sendData, "%f,%f,%f,%f,%f", sendControlData.aileron,sendControlData.elevator,sendControlData.rudder,sendControlData.throttle[0],sendControlData.throttle[1]);
			printf("%s\n", sendData);
			
			nlen = strlen(sendData);
			sendData[nlen] = '\n';

			sendData[nlen + 1] = 0;
			sendlen = sendto(sClient, (char*)sendData, strlen(sendData), 0, (struct sockaddr*)&sclient, sizeof(struct sockaddr));
			ret = GetLastError();
			memset(sendData, 0, 1024);

		}

	}
	fclose(fp);
	closesocket(sClient);

	return 0;
}

DWORD WINAPI thread_interactive(LPVOID lpThreadParameter)
{
	while (1)
	{
		Sleep(1);
	}
	return 0;
}
int main(void)
{
	WORD sockVersion = MAKEWORD(2, 2);
	WSADATA wsadata;
	if (WSAStartup(sockVersion, &wsadata) != 0)
	{
		printf("WinSock startup failed!\n");
		return 0;
	}
	DWORD thread_udp_receive_id, thread_procer_id, thread_interactive_id;
	fg_data_Mutex = CreateMutex(NULL,FALSE,NULL);//互斥锁
	rec_flag_Mutex = CreateMutex(NULL,FALSE,NULL);

	memset((void*)&g_FgData,0,sizeof(struct FGAlldata));
	system("pause");
	HANDLE thread_udp_handle = CreateThread(NULL, 0, thread_udp_receive, NULL, 0, &thread_udp_receive_id);
	HANDLE thread_pro_handle = CreateThread(NULL, 0, thread_procer, NULL, 0, &thread_procer_id);
	HANDLE thread_iter_handle = CreateThread(NULL, 0, thread_interactive, NULL, 0, &thread_interactive_id);

	WaitForSingleObject(thread_udp_handle, INFINITE);
	WaitForSingleObject(thread_pro_handle, INFINITE);
	WaitForSingleObject(thread_iter_handle, INFINITE);

	CloseHandle(thread_udp_handle);
	CloseHandle(thread_pro_handle);
	CloseHandle(thread_iter_handle);

	system("pause");
	WSACleanup();
	return 0;


}
