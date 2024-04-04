export const load = async ( { params } ) => {
    const post = await getPost(params.postId);
    return { post };
}

//db example
// const getPosts = async (postId) => {
//     const db = await connectToDatabase();
//     const posts = await db.collection('posts');
//     const post = await posts.findOne({ postId });
//     return post;
// }

// db example
const getPost = async (id) => {
    console.log('id', id);
    const post = await fetch(`https://jsonplaceholder.typicode.com/posts/${id}`);
    return await post.json();
}
