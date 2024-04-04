export const load = async () => {
    const posts = await fetch('https://jsonplaceholder.typicode.com/posts');
    const thinksResult = thinks(); // thinks 함수 호출
    return { 
        posts: await posts.json(),
        title: await thinksResult.title,
    };
}


const thinks = () => {
    return {
        title: 'Hello from thinks',
        description: 'This is a description from thinks'
    }
}