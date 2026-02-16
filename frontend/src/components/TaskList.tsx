'use client';

import { Task } from '../types/task';
import { updateTask, deleteTask } from '../lib/api';
import { useState } from 'react';

interface TaskListProps {
  tasks: Task[];
  onTasksChanged: () => void;
}

export default function TaskList({ tasks, onTasksChanged }: TaskListProps) {
  const [updatingId, setUpdatingId] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const handleToggleComplete = async (task: Task) => {
    setUpdatingId(task.id);
    try {
      await updateTask(task.id, { completed: !task.completed });
      onTasksChanged();
    } catch (err) {
      console.error('Error updating task:', err);
    } finally {
      setUpdatingId(null);
    }
  };

  const handleDelete = async (taskId: string) => {
    setDeletingId(taskId);
    try {
      await deleteTask(taskId);
      onTasksChanged();
    } catch (err) {
      console.error('Error deleting task:', err);
    } finally {
      setDeletingId(null);
    }
  };

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        No tasks yet. Add one above to get started!
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {tasks.map((task) => (
        <div
          key={task.id}
          className="flex items-center gap-3 p-4 bg-white border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
        >
          <input
            type="checkbox"
            checked={task.completed}
            onChange={() => handleToggleComplete(task)}
            disabled={updatingId === task.id}
            className="w-5 h-5 text-blue-500 rounded focus:ring-2 focus:ring-blue-500 cursor-pointer"
          />
          <span
            className={`flex-1 ${
              task.completed
                ? 'line-through text-gray-400'
                : 'text-gray-800'
            }`}
          >
            {task.title}
          </span>
          <button
            onClick={() => handleDelete(task.id)}
            disabled={deletingId === task.id}
            className="px-3 py-1 text-sm text-red-600 hover:bg-red-50 rounded disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {deletingId === task.id ? 'Deleting...' : 'Delete'}
          </button>
        </div>
      ))}
    </div>
  );
}
