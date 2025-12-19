export async function getTaskStatus(taskId) {
    try {
        const response = await fetch(`/api/tasks/${taskId}`);
        if (!response.ok) throw new Error('Error fetching task status');
        return await response.json();
    } catch (error) {
        console.error('Task API Error:', error);
        throw error;
    }
}

export function pollTask(taskId, onProgress, onComplete, onError) {
    const interval = setInterval(async () => {
        try {
            const data = await getTaskStatus(taskId);

            if (data.status === 'PROGRESS') {
                if (data.info && data.info.message) {
                    onProgress(data.info.message);
                }
            } else if (data.status === 'SUCCESS' || data.status === 'FAILURE') {
                clearInterval(interval);
                if (data.result && data.result.status === 'error') {
                    onError(data.result.error);
                } else if (data.status === 'FAILURE') {
                    onError('Task Failed in Celery');
                } else {
                    onComplete(data.result);
                }
            } else {
                // PENDING or STARTED
                // Do nothing
            }
        } catch (err) {
            clearInterval(interval);
            onError(err.message);
        }
    }, 2000); // Poll every 2s

    // Return cancel function
    return () => clearInterval(interval);
}
