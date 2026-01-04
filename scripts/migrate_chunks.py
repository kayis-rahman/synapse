#!/usr/bin/env python3
"""
Migrate chunks.json from pi-rag to synapse project.

Updates:
1. project_id: "pi-rag" → project_id: "synapse"
2. source: "/home/dietpi/pi-rag/..." → source: "/home/dietpi/synapse/..."
3. metadata.project: "pi-rag" → metadata.project: "synapse"
"""

import json
import sys
from pathlib import Path

def migrate_chunks(input_path: str, output_path: str) -> dict:
    """
    Migrate chunks.json from pi-rag to synapse.

    Returns:
        dict: Statistics about changes made
    """
    with open(input_path, 'r') as f:
        chunks = json.load(f)

    stats = {
        'total_chunks': len(chunks),
        'pi_rag_project_id': 0,
        'pi_rag_source_path': 0,
        'pi_rag_project_metadata': 0
    }

    for chunk in chunks:
        # Update project_id in metadata
        if chunk.get('metadata', {}).get('project_id') == 'pi-rag':
            chunk['metadata']['project_id'] = 'synapse'
            stats['pi_rag_project_id'] += 1

        # Update source path
        if 'source' in chunk['metadata'] and '/home/dietpi/pi-rag' in chunk['metadata']['source']:
            chunk['metadata']['source'] = chunk['metadata']['source'].replace(
                '/home/dietpi/pi-rag',
                '/home/dietpi/synapse'
            )
            stats['pi_rag_source_path'] += 1

        # Update project in metadata
        if chunk.get('metadata', {}).get('project') == 'pi-rag':
            chunk['metadata']['project'] = 'synapse'
            stats['pi_rag_project_metadata'] += 1

    # Write updated chunks
    with open(output_path, 'w') as f:
        json.dump(chunks, f, indent=2)

    return stats


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 migrate_chunks.py <chunks.json>")
        sys.exit(1)

    chunks_path = sys.argv[1]
    backup_path = f"{chunks_path}.backup"

    # Create backup
    print(f"Backing up {chunks_path} to {backup_path}...")
    Path(chunks_path).replace(backup_path)

    # Migrate
    print(f"Migrating {chunks_path}...")
    stats = migrate_chunks(backup_path, chunks_path)

    # Print statistics
    print("\n" + "="*60)
    print("MIGRATION COMPLETE")
    print("="*60)
    print(f"Total chunks: {stats['total_chunks']}")
    print(f"Updated project_id: {stats['pi_rag_project_id']}")
    print(f"Updated source paths: {stats['pi_rag_source_path']}")
    print(f"Updated project metadata: {stats['pi_rag_project_metadata']}")
    print("="*60)


if __name__ == '__main__':
    main()
