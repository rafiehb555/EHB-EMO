#!/usr/bin/env python3
"""
EHB AI Agent Base Tests
"""

import pytest
import asyncio
from ai_agents.core.agent_base import AIAgentBase

class TestAgent(AIAgentBase):
    async def process_input(self, input_data):
        return {"response": "test response"}
    
    async def learn(self, experience):
        return True
    
    async def plan(self, goal):
        return ["step1", "step2"]
    
    async def execute(self, action):
        return {"result": "executed"}

@pytest.mark.asyncio
async def test_agent_creation():
    """Test agent creation"""
    agent = TestAgent("test_agent", "Test Agent", ["test_capability"])
    assert agent.agent_id == "test_agent"
    assert agent.name == "Test Agent"
    assert agent.is_active == True

@pytest.mark.asyncio
async def test_agent_status():
    """Test agent status"""
    agent = TestAgent("test_agent", "Test Agent", ["test_capability"])
    status = agent.get_status()
    assert "agent_id" in status
    assert "name" in status
    assert "capabilities" in status

@pytest.mark.asyncio
async def test_agent_processing():
    """Test agent input processing"""
    agent = TestAgent("test_agent", "Test Agent", ["test_capability"])
    response = await agent.process_input({"test": "data"})
    assert "response" in response

@pytest.mark.asyncio
async def test_agent_learning():
    """Test agent learning"""
    agent = TestAgent("test_agent", "Test Agent", ["test_capability"])
    result = await agent.learn({"experience": "test"})
    assert result == True

@pytest.mark.asyncio
async def test_agent_planning():
    """Test agent planning"""
    agent = TestAgent("test_agent", "Test Agent", ["test_capability"])
    plan = await agent.plan("test goal")
    assert isinstance(plan, list)
    assert len(plan) > 0

@pytest.mark.asyncio
async def test_agent_execution():
    """Test agent execution"""
    agent = TestAgent("test_agent", "Test Agent", ["test_capability"])
    result = await agent.execute("test action")
    assert "result" in result