import requests
from typing import List, Dict
from config import *
import json
import socket
import netifaces
import subprocess

class LocationService:
    def __init__(self):
        self.ak = BAIDU_MAP_AK
        self.base_url = "https://api.map.baidu.com/place/v2/search"
        # 从配置文件加载默认位置
        self.default_location = DEFAULT_LOCATION
        
    def get_current_location(self) -> str:
        """
        获取当前位置的经纬度，按优先级尝试不同定位方式
        1. 连接的WiFi定位
        2. 外网IP定位
        3. 默认位置
        """
        try:
            # 1. 尝试通过WiFi定位
            wifi_location = self._get_location_by_wifi()
            if wifi_location:
                return wifi_location
                
            # 2. 尝试通过IP定位
            ip_location = self._get_location_by_ip()
            if ip_location:
                return ip_location
                
        except Exception as e:
            print(f"定位错误: {e}")
        
        # 3. 使用默认位置
        print("使用默认位置")
        return self.default_location
        
    def _get_location_by_wifi(self) -> str:
        """通过WiFi信息获取位置"""
        try:
            # 获取当前连接的WiFi信息
            wifi_info = self._get_wifi_info()
            if not wifi_info:
                return None
                
            # 调用百度地图WiFi定位API
            url = "https://api.map.baidu.com/location/api/v2/sdk"
            params = {
                "ak": self.ak,
                "macs": wifi_info["bssid"],
                "output": "json"
            }
            
            response = requests.get(url, params=params)
            result = response.json()
            
            if result["status"] == 0:
                location = result["content"]["point"]
                return f"{location['x']},{location['y']}"
                
        except Exception as e:
            print(f"WiFi定位失败: {e}")
        return None
        
    def _get_wifi_info(self) -> Dict:
        """获取当前连接的WiFi信息"""
        try:
            # 使用iwconfig命令获取WiFi信息
            result = subprocess.run(['iwconfig'], capture_output=True, text=True)
            if 'ESSID' in result.stdout:
                # 解析WiFi信息
                lines = result.stdout.split('\n')
                info = {}
                for line in lines:
                    if 'ESSID' in line:
                        info['ssid'] = line.split('ESSID:')[1].strip('"')
                    elif 'Access Point' in line:
                        info['bssid'] = line.split('Access Point:')[1].strip()
                return info
        except Exception as e:
            print(f"获取WiFi信息失败: {e}")
        return None

    def _get_location_by_ip(self) -> str:
        """通过IP地址获取位置"""
        try:
            # 获取外网IP
            external_ip = self._get_external_ip()
            if not external_ip:
                return None
                
            # 调用百度地图IP定位API
            url = f"https://api.map.baidu.com/location/ip"
            params = {
                "ak": self.ak,
                "ip": external_ip,
                "coor": "bd09ll"
            }
            
            response = requests.get(url, params=params)
            result = response.json()
            
            if result["status"] == 0:
                content = result["content"]
                return f"{content['point']['x']},{content['point']['y']}"
                
        except Exception as e:
            print(f"IP定位失败: {e}")
        return None
        
    def _get_external_ip(self) -> str:
        """获取外网IP地址"""
        try:
            response = requests.get('https://api.ipify.org')
            return response.text
        except:
            return None

    def search_nearby_places(self, query: str, location: str = None, radius: int = 2000) -> List[Dict]:
        """
        搜索附近的地点
        :param query: 搜索关键词（如"美食"、"火锅"等）
        :param location: 位置坐标（经度,纬度），如果为None则使用IP定位
        :param radius: 搜索半径，单位米
        :return: 地点列表
        """
        try:
            if location is None:
                location = self.get_current_location()
                
            params = {
                "query": query,
                "location": location,
                "radius": radius,
                "output": "json",
                "ak": self.ak,
                "scope": 2,  # 返回详细信息
                "page_size": 10
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            result = response.json()
            
            if result["status"] == 0:
                return self._format_places(result["results"])
            else:
                print(f"百度地图API错误: {result['message']}")
                return []
                
        except Exception as e:
            print(f"搜索位置时出错: {e}")
            return []
    
    def _format_places(self, places: List[Dict]) -> List[Dict]:
        """格式化地点信息"""
        formatted_places = []
        for place in places:
            formatted_place = {
                "name": place["name"],
                "address": place["address"],
                "distance": f"{place.get('detail_info', {}).get('distance', '未知')}米",
                "rating": f"{place.get('detail_info', {}).get('overall_rating', '暂无')}分",
                "price": f"￥{place.get('detail_info', {}).get('price', '未知')}/人",
                "tags": place.get("detail_info", {}).get("tag", "").split(";"),
            }
            formatted_places.append(formatted_place)
        return formatted_places

    def format_response(self, places: List[Dict]) -> str:
        """将地点列表格式化为语音回复文本"""
        if not places:
            return "抱歉，我没有找到符合条件的地点。"
            
        response = "我为您找到以下推荐：\n"
        for i, place in enumerate(places[:5], 1):  # 只取前5个结果
            response += f"{i}. {place['name']}\n"
            response += f"   地址：{place['address']}\n"
            response += f"   距离：{place['distance']}\n"
            if place['rating'] != '暂无分':
                response += f"   评分：{place['rating']}\n"
            if place['price'] != '￥未知/人':
                response += f"   人均：{place['price']}\n"
            response += "\n"
            
        return response 