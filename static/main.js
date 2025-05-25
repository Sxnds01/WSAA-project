const addHabit = async (event) => {
    event.preventDefault();

    const name = document.getElementById('habitName').value;
    const date = document.getElementById('habitDate').value;
    
    const newHabit = {
        name: name,
        date: date,
        completed: false  
    };

    const response = await fetch('/api/habits', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newHabit)
    });

    if (response.ok) {
        console.log('Habit added successfully');
    } else {
        console.error('Failed to add habit');
    }
};
document.addEventListener('DOMContentLoaded', fetchHabits);