"""
Smart AI Namer 테스트
"""

import pytest
from PIL import Image
import numpy as np
import sys
import os

# app.py의 함수들을 임포트하기 위해 경로 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import extract_date, preprocess_image_advanced


class MockUploadedFile:
    """파일 업로드 객체 모킹"""
    def __init__(self, name):
        self.name = name


def test_extract_date_from_filename():
    """파일명에서 날짜 추출 테스트"""
    mock_file = MockUploadedFile("2024-12-25_report.png")
    img = Image.new('RGB', (100, 100), 'white')
    
    date = extract_date(mock_file, img)
    assert date == "2024.12.25"


def test_extract_date_no_pattern():
    """날짜 패턴이 없는 파일명 테스트"""
    mock_file = MockUploadedFile("document.png")
    img = Image.new('RGB', (100, 100), 'white')
    
    date = extract_date(mock_file, img)
    # 현재 날짜가 반환되어야 함
    assert len(date) == 10  # YYYY.MM.DD 형식
    assert date.count('.') == 2


def test_preprocess_image_small():
    """작은 이미지 전처리 테스트 (자동 확대)"""
    img = Image.new('RGB', (500, 500), 'white')
    processed = preprocess_image_advanced(img)
    
    # 1000픽셀 이상으로 확대되었는지 확인
    assert processed.size[0] >= 1000 or processed.size[1] >= 1000


def test_preprocess_image_large():
    """큰 이미지 전처리 테스트"""
    img = Image.new('RGB', (2000, 2000), 'white')
    processed = preprocess_image_advanced(img)
    
    # 이미지가 처리되었는지 확인 (None이 아님)
    assert processed is not None
    # 크기 유지 확인
    assert processed.size[0] == 2000 or processed.size[1] == 2000


def test_preprocess_image_grayscale():
    """그레이스케일 이미지 전처리 테스트"""
    img = Image.new('L', (1000, 1000), 'white')
    processed = preprocess_image_advanced(img)
    
    assert processed is not None
    # 모드 확인 (L: grayscale)
    assert processed.mode in ['L', '1']


def test_preprocess_image_returns_pil():
    """전처리 결과가 PIL 이미지인지 확인"""
    img = Image.new('RGB', (1000, 1000), 'white')
    processed = preprocess_image_advanced(img)
    
    assert isinstance(processed, Image.Image)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
