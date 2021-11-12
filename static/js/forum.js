var postsTemp = [
    {
        id: 1,
        title: "Thread 1", 
        author: "John", 
        date: Date.now(), 
        content: "Post content", 
        comments: [
            {
                author: "Jim", 
                date: Date.now(), 
                content: "Hey"
            }, 
            {
                author: "Bill", 
                date: Date.now(), 
                content: "Hey there"
            }, 
        ]
    }, 
    {
        id: 2,
        title: "Thread 2", 
        author: "Jim", 
        date: Date.now(), 
        content: "Post content 2", 
        comments: [
            {
                author: "Jim", 
                date: Date.now(), 
                content: "Hey"
            }, 
            {
                author: "Bill", 
                date: Date.now(), 
                content: "Hey there"
            }, 
        ]
    }, 
    {
        id: 3,
        title: "Thread 3", 
        author: "Bob", 
        date: Date.now(), 
        content: "Post content 3", 
        comments: [
            {
                author: "Jim", 
                date: Date.now(), 
                content: "Hey"
            }, 
            {
                author: "Bill", 
                date: Date.now(), 
                content: "Hey there"
            }, 
        ]
    }
]

var posts = postsTemp;
if (sessionStorage && sessionStorage.getItem('posts')) {
    posts = JSON.parse(sessionStorage.getItem('posts'));
}
else {
    posts = postsTemp;
    sessionStorage.setItem('posts', JSON.stringify(postsTemp));
}