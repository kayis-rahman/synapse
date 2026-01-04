"""Test episodic memory functionality"""
import pytest
import tempfile
import os
from datetime import datetime, timedelta


def test_store_episode():
    """Test storing an episodic memory episode"""
    from synapse.rag.episodic_store import EpisodicStore, Episode
    
    with tempfile.NamedTemporaryFile(suffix='.db') as temp_db:
        store = EpisodicStore(temp_db)
        
        episode = Episode(
            project_id="test",
            situation="Test situation",
            action="Test action",
            outcome="Test outcome",
            lesson="Test lesson",
            confidence=0.9
        )
        
        stored_episode = store.store_episode(episode)
        
        assert stored_episode.id is not None
        assert stored_episode.project_id == "test"
        assert stored_episode.situation == "Test situation"
        assert stored_episode.action == "Test action"
        assert stored_episode.outcome == "Test outcome"
        assert stored_episode.lesson == "Test lesson"
        assert stored_episode.confidence == 0.9


def test_list_recent_episodes():
    """Test listing recent episodes for a project"""
    from synapse.rag.episodic_store import EpisodicStore
    
    with tempfile.NamedTemporaryFile(suffix='.db') as temp_db:
        store = EpisodicStore(temp_db)
        
        # Store multiple episodes
        for i in range(3):
            episode = Episode(
                project_id="test",
                situation=f"Situation {i}",
                action=f"Action {i}",
                outcome=f"Outcome {i}",
                lesson=f"Lesson {i}",
                confidence=0.8
            )
            store.store_episode(episode)
        
        # List recent episodes
        episodes = store.list_recent_episodes(
            project_id="test",
            days=30,
            min_confidence=0.0,
            limit=5
        )
        
        assert len(episodes) == 3


def test_query_episodes_by_lesson():
    """Test querying episodes by lesson content"""
    from synapse.rag.episodic_store import EpisodicStore
    
    with tempfile.NamedTemporaryFile(suffix='.db') as temp_db:
        store = EpisodicStore(temp_db)
        
        # Store episodes with different lesson types
        lesson_types = ["success", "pattern", "mistake", "failure"]
        for lesson_type in lesson_types:
            episode = Episode(
                project_id="test",
                situation="Test situation",
                action="Test action",
                outcome="Test outcome",
                lesson=f"Lesson about {lesson_type}",
                confidence=0.85,
                lesson_type=lesson_type
            )
            store.store_episode(episode)
        
        # Query by lesson
        for lesson_type in lesson_types:
            episodes = store.query_episodes(
                project_id="test",
                lesson=lesson_type,
                min_confidence=0.0,
                limit=10
            )
            assert len(episodes) == 1
            assert episodes[0].lesson_type == lesson_type


def test_update_episode():
    """Test updating an existing episode"""
    from synapse.rag.episodic_store import EpisodicStore
    
    with tempfile.NamedTemporaryFile(suffix='.db') as temp_db:
        store = EpisodicStore(temp_db)
        
        # Store initial episode
        episode = Episode(
            project_id="test",
            situation="Initial situation",
            action="Initial action",
            outcome="Initial outcome",
            lesson="Initial lesson",
            confidence=0.7
        )
        stored_episode = store.store_episode(episode)
        
        # Update the episode
        stored_episode.action = "Updated action"
        stored_episode.outcome = "Updated outcome"
        stored_episode.confidence = 0.95
        
        updated = store.update_episode(stored_episode)
        
        assert updated.action == "Updated action"
        assert updated.outcome == "Updated outcome"
        assert updated.confidence == 0.95


def test_query_episodes_by_project():
    """Test querying episodes by project_id"""
    from synapse.rag.episodic_store import EpisodicStore
    
    with tempfile.NamedTemporaryFile(suffix='.db') as temp_db:
        store = EpisodicStore(temp_db)
        
        # Store episodes for different projects
        for project_id in ["test", "other"]:
            episode = Episode(
                project_id=project_id,
                situation=f"Situation for {project_id}",
                action=f"Action for {project_id}",
                outcome=f"Outcome for {project_id}",
                lesson=f"Lesson for {project_id}",
                confidence=0.8
            )
            store.store_episode(episode)
        
        # Query by project_id
        episodes = store.query_episodes(project_id="test")
        assert len(episodes) == 1
        assert episodes[0].project_id == "test"
