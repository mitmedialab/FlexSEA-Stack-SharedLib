/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'plan-gui' Graphical User Interface
	Copyright (C) 2017 Dephy, Inc. <http://dephy.com/>
*****************************************************************************
	[Lead developper] Jean-Francois (JF) Duval, jfduval at dephy dot com.
	[Origin] Based on Jean-Francois Duval's work at the MIT Media Lab
	Biomechatronics research group <http://biomech.media.mit.edu/>
	[Contributors]
*****************************************************************************
	[This file] flexsea_board: configuration and functions for this
	particular board
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2016-09-09 | jfduval | Initial GPL-3.0 release
	*
****************************************************************************/

#ifdef __cplusplus
extern "C" {
#endif

//****************************************************************************
// Include(s)
//****************************************************************************

#include <stdio.h>
#include "flexsea_config.h"
#include <stdint.h>
#include "flexsea.h"
#include "flexsea_board.h"
#include "../../flexsea-system/inc/flexsea_system.h"
#include "flexsea_user_structs.h"
#include "flexsea_cmd_user.h"
#include "flexsea_payload.h"
#include "cmd-Rigid.h"

//****************************************************************************
// Local variable(s)
//****************************************************************************

void (*externalSendSerialSlave)(PacketWrapper* p) = NULL;
void (*externalSendSerialMaster)(PacketWrapper* p) = NULL;

//****************************************************************************
// Private function prototype(s)
//****************************************************************************

static void flexsea_send_serial_null(PacketWrapper* p);
static void coreFlexSEAInit(uint8_t id);

//****************************************************************************
// Function(s)
//****************************************************************************

//This function needs to be called at the start of the host program.
//id: sets the board_id variable. Typically, it will be FLEXSEA_PLAN_1
//fsss: name of your flexsea_send_serial_slave implementation
//fssm: name of your flexsea_send_serial_master implementation
//Ex.: initFlexSEAStack(FLEXSEA_PLAN_1, flexsea_send_serial_slave,
//						flexsea_send_serial_master);
void initFlexSEAStack(uint8_t id, void (*fsss)(PacketWrapper* p), \
						void (*fssm)(PacketWrapper* p))
{
	coreFlexSEAInit(id);
	mapSendSerialSlave(fsss);
	mapSendSerialMaster(fssm);
}

//If you do not wish to provide fsss & fssm, use this version.
//Note: you won't be able to use packAndSend(). Use pack() and 'manually'
//send and receive your packets.
void initFlexSEAStack_minimalist(uint8_t id)
{
	coreFlexSEAInit(id);
	//Default catch - won't crash, but won't send data:
	mapSendSerialSlave(flexsea_send_serial_null);
	mapSendSerialMaster(flexsea_send_serial_null);
}

//Prepares the structures:
void initMasterCommDefaults(void)
{
	//SPI:
	initCommPeriph(&commPeriph[PORT_SPI], PORT_SPI, MASTER, rx_buf_3, \
				comm_str_3, rx_command_3, &rx_buf_circ_3, \
				&packet[PORT_SPI][INBOUND], &packet[PORT_SPI][OUTBOUND]);

	//USB:
	initCommPeriph(&commPeriph[PORT_USB], PORT_USB, MASTER, rx_buf_4, \
			comm_str_4, rx_command_4, &rx_buf_circ_4, \
			&packet[PORT_USB][INBOUND], &packet[PORT_USB][OUTBOUND]);

	//Bluetooth:
	initCommPeriph(&commPeriph[PORT_WIRELESS], PORT_WIRELESS, MASTER, rx_buf_5, \
				comm_str_5, rx_command_5, &rx_buf_circ_5, \
				&packet[PORT_WIRELESS][INBOUND], &packet[PORT_WIRELESS][OUTBOUND]);
}

void initSlaveCommDefaults(void)
{
	//RS-485 #1:
	initCommPeriph(&commPeriph[PORT_RS485_1], PORT_RS485_1, SLAVE, rx_buf_1, \
			comm_str_1, rx_command_1, &rx_buf_circ_1, \
			&packet[PORT_RS485_1][INBOUND], &packet[PORT_RS485_1][OUTBOUND]);

	//UART:
	initCommPeriph(&commPeriph[PORT_RS485_2], PORT_RS485_2, SLAVE, rx_buf_2, \
			comm_str_2, rx_command_2, &rx_buf_circ_2, \
			&packet[PORT_RS485_2][INBOUND], &packet[PORT_RS485_2][OUTBOUND]);
}

void mapSendSerialSlave(void (*f)(PacketWrapper* p))
{
	externalSendSerialSlave = f;
}

void mapSendSerialMaster(void (*f)(PacketWrapper* p))
{
	externalSendSerialMaster = f;
}

//Returns the previous board ID, then changes it to be 'id'
uint8_t setBoardID(uint8_t id)
{
	uint8_t tmp = board_id;
	board_id = id;
	return tmp;
}

//****************************************************************************
// Private Function(s)
//****************************************************************************

//When the Host code doesn't want to implement flexsea_send_serial_x() we
//redirect the code here:
static void flexsea_send_serial_null(PacketWrapper* p){};

static void coreFlexSEAInit(uint8_t id)
{
	init_flexsea_payload_ptr();
	initMasterCommDefaults();
	initSlaveCommDefaults();
	initializeGlobalStructs();
	initializeUserStructs();

	init_rigid();

	setBoardID(id);
}

#ifdef __cplusplus
}
#endif
