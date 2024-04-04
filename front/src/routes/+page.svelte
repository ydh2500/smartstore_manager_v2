<script>
    export let data;
    console.log(data);
</script>

<h1>Home Page</h1>

<ul>
    {#each data.posts as post}
        <li>
            <a href={post.id}>{post.title}{data.title}</a>
        </li>
    {/each}



</ul>

<style>
    /* Add any necessary styles here */
</style>