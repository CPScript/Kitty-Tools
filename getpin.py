# ANOTHER ATTEMPT TO MAKE A "quizid" from "game pin" grabber using the API websockets that kahoot provides

#!/usr/bin/env python3

import asyncio
import json
import aiohttp
import websockets
from typing import Optional, Dict, Any
import sys
import argparse


class KahootPinResolver: # Handles Kahoot pin to quiz ID resolution via WebSocket API    
    def __init__(self):
        self.session_token = None
        self.quiz_id = None
        
    async def get_session_info(self, pin: str) -> Optional[Dict[str, Any]]:
        """
        Get session information from Kahoot pin
        Returns session data including quiz ID
        """
        try:
            # Step 1: Get session token from REST API
            async with aiohttp.ClientSession() as session:
                url = f"https://kahoot.it/reserve/session/{pin}/?{pin}"
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'application/json',
                    'Referer': 'https://kahoot.it/'
                }
                
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        print(f"Error: Failed to get session info (HTTP {response.status})")
                        return None
                    
                    data = await response.json()
                    self.session_token = data.get('token')
                    
                    if not self.session_token:
                        print("Error: No session token received")
                        return None
                    
                    return data
                    
        except aiohttp.ClientError as e:
            print(f"Network error: {e}")
            return None
        except json.JSONDecodeError:
            print("Error: Invalid JSON response")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    async def connect_websocket(self, pin: str) -> Optional[str]:
        """
        Connect to Kahoot WebSocket and extract quiz ID
        Returns quiz ID if successful
        """
        if not self.session_token:
            print("Error: No session token available")
            return None
            
        try:
            # WebSocket connection to get detailed quiz info
            ws_url = f"wss://kahoot.it/cometd/{pin}/{self.session_token}"
            
            async with websockets.connect(ws_url) as websocket:
                # Send handshake message
                handshake_msg = [{
                    "channel": "/meta/handshake",
                    "version": "1.0",
                    "minimumVersion": "1.0beta",
                    "supportedConnectionTypes": ["websocket", "long-polling"],
                    "id": "1"
                }]
                
                await websocket.send(json.dumps(handshake_msg))
                response = await websocket.recv()
                handshake_data = json.loads(response)
                
                if not handshake_data[0].get('successful'):
                    print("Error: WebSocket handshake failed")
                    return None
                
                client_id = handshake_data[0].get('clientId')
                
                # Subscribe to controller channel
                subscribe_msg = [{
                    "channel": "/meta/subscribe",
                    "clientId": client_id,
                    "subscription": "/service/controller",
                    "id": "2"
                }]
                
                await websocket.send(json.dumps(subscribe_msg))
                response = await websocket.recv()
                
                # Connect to get quiz data
                connect_msg = [{
                    "channel": "/meta/connect",
                    "clientId": client_id,
                    "connectionType": "websocket",
                    "id": "3"
                }]
                
                await websocket.send(json.dumps(connect_msg))
                
                # Wait for quiz data
                timeout_counter = 0
                while timeout_counter < 10:  # 10 second timeout
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                        data = json.loads(response)
                        
                        # Look for quiz ID in response
                        for message in data:
                            if 'data' in message and message['data']:
                                quiz_data = message['data']
                                if 'quizId' in quiz_data:
                                    return quiz_data['quizId']
                                elif 'id' in quiz_data:
                                    return quiz_data['id']
                                    
                    except asyncio.TimeoutError:
                        timeout_counter += 1
                        continue
                    except json.JSONDecodeError:
                        continue
                
                print("Error: Quiz ID not found in WebSocket data")
                return None
                
        except websockets.exceptions.WebSocketException as e:
            print(f"WebSocket error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected WebSocket error: {e}")
            return None
    
    async def resolve_pin(self, pin: str) -> Optional[str]:
        """
        Main method to resolve Kahoot pin to quiz ID
        Returns quiz ID string if successful
        """
        print(f"Resolving pin: {pin}")
        
        # Get session info first
        session_info = await self.get_session_info(pin)
        if not session_info:
            return None
            
        # Try WebSocket approach for quiz ID
        quiz_id = await self.connect_websocket(pin)
        if quiz_id:
            self.quiz_id = quiz_id
            return quiz_id
            
        # Fallback: check if quiz ID is in session info
        if 'quizId' in session_info:
            self.quiz_id = session_info['quizId']
            return self.quiz_id
        elif 'id' in session_info:
            self.quiz_id = session_info['id']
            return self.quiz_id
            
        print("Error: Could not extract quiz ID from any source")
        return None


async def main():
    parser = argparse.ArgumentParser(description='Convert Kahoot pin to quiz ID')
    parser.add_argument('pin', help='Kahoot game pin')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if not args.pin.isdigit():
        print("Error: Pin must be numeric")
        sys.exit(1)
    
    resolver = KahootPinResolver()
    
    try:
        quiz_id = await resolver.resolve_pin(args.pin)
        
        if quiz_id:
            print(f"Success!")
            print(f"Pin: {args.pin}")
            print(f"Quiz ID: {quiz_id}")
            
            if args.verbose:
                print(f"Session Token: {resolver.session_token}")
                
        else:
            print("Failed to resolve quiz ID")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # dependencies check YAYAYYAYAYYAYAYYAYYAYAYYAYYAYAYYAAYYAY AHAHAHHAHAHAHHAHAHHAHHAHAH BLEHHHH :P
    required_modules = ['aiohttp', 'websockets']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print("Missing required dependencies:")
        for module in missing_modules:
            print(f"  pip install {module}")
        sys.exit(1)
    
    asyncio.run(main())
