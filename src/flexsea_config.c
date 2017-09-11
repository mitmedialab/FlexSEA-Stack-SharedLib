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

//#include "main.h"
#include "flexsea_board.h"
#include "../../flexsea-system/inc/flexsea_system.h"


//****************************************************************************
// Local variable(s)
//****************************************************************************


//****************************************************************************
// External variable(s)
//****************************************************************************



//****************************************************************************
// Function(s)
//****************************************************************************

void mapSendSerialSlave(void (*f)(PacketWrapper* p))
{
	printf("Mapping...\n");
	externalSendSerialSlave = f;
}

//Returns the previous board ID, then changes it to be 'id'
uint8_t setBoardID(uint8_t id)
{
	uint8_t tmp = board_id;
	board_id = id;
	return tmp;
}

#ifdef __cplusplus
}
#endif
