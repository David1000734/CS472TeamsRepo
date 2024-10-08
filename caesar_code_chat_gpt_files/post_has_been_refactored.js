import { auth, db } from "/utils/firebase";
import { useAuthState } from "react-firebase-hooks/auth";
import { useRouter } from "next/router";
import { useEffect, useReducer, useState, useCallback } from "react";
import {
  addDoc,
  collection,
  doc,
  serverTimestamp,
  updateDoc,
} from "firebase/firestore";
import { toast } from "react-toastify";
import Spinner from "/components/spinner";

// Post reducer for state management
const postReducer = (state, action) => {
  switch (action.type) {
    case "SET_DESCRIPTION":
      return { ...state, description: action.payload };
    case "SET_POST":
      return { ...state, description: action.payload.description, id: action.payload.id };
    case "RESET_POST":
      return { description: "" };
    default:
      return state;
  }
};

const Post = () => {
  const [post, dispatch] = useReducer(postReducer, { description: "" });
  const [user, loading] = useAuthState(auth);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const route = useRouter();
  const routeData = route.query;

  // Centralized and flexible post validation
  const validatePost = (post, rules = { maxLength: 300 }) => {
    if (!post.description) {
      toast.error("Description field is empty 😅", {
        position: toast.POSITION.TOP_CENTER,
        autoClose: 500,
      });
      return false;
    }
    if (post.description.length > rules.maxLength) {
      toast.error(`Description exceeds ${rules.maxLength} characters 😅`, {
        position: toast.POSITION.TOP_CENTER,
        autoClose: 500,
      });
      return false;
    }
    return true;
  };

  // Submit post function with error handling and loading state
  const submitPost = useCallback(
    async (e) => {
      e.preventDefault();
      if (!validatePost(post)) return;

      setIsSubmitting(true);
      try {
        if (post.id) {
          // Update existing post
          const docRef = doc(db, "posts", post.id);
          await updateDoc(docRef, { ...post, timestamp: serverTimestamp() });
          toast.success("Post has been updated 😃", {
            position: toast.POSITION.TOP_CENTER,
            autoClose: 500,
          });
        } else {
          // Create new post
          const collectionRef = collection(db, "posts");
          await addDoc(collectionRef, {
            ...post,
            timestamp: serverTimestamp(),
            user: user.uid,
            avatar: user.photoURL,
            username: user.displayName,
          });
          toast.success("Post has been made 😃", {
            position: toast.POSITION.TOP_CENTER,
            autoClose: 500,
          });
        }
        dispatch({ type: "RESET_POST" });
        route.push("/");
      } catch (error) {
        console.error("Error submitting post:", error);
        toast.error("Something went wrong. Please try again.", {
          position: toast.POSITION.TOP_CENTER,
          autoClose: 500,
        });
      } finally {
        setIsSubmitting(false);
      }
    },
    [post, user, route]
  );

  // User authentication and post loading logic
  useEffect(() => {
    if (loading) return;

    if (!user) {
      route.push("/auth/login");
    } else if (routeData.id) {
      dispatch({ type: "SET_POST", payload: { description: routeData.description, id: routeData.id } });
    }
  }, [user, loading, routeData, route]);

  return (
    <>
      {loading ? (
        <Spinner />
      ) : (
        <div className="my-20 p-12 shadow-lg rounded-lg max-w-md mx-auto">
          <PostForm post={post} isSubmitting={isSubmitting} onSubmit={submitPost} onChange={(e) => dispatch({ type: "SET_DESCRIPTION", payload: e.target.value })} />
        </div>
      )}
    </>
  );
};

// Form component with memoization
const PostForm = React.memo(({ post, isSubmitting, onSubmit, onChange }) => (
  <form onSubmit={onSubmit}>
    <h1 className="text-2xl font-bold">
      {post.id ? "Edit your post" : "Create a new post"}
    </h1>
    <div className="py-2">
      <h3 className="text-lg font-medium py-2">Description</h3>
      <textarea
        value={post.description}
        onChange={onChange}
        className="bg-gray-800 h-48 w-full text-white rounded-lg p-2 text-sm"
      ></textarea>
      <p
        className={`text-cyan-600 font-medium text-sm ${
          post.description.length > 300 ? "text-red-600" : ""
        }`}
      >
        {post.description.length}/300
      </p>
    </div>
    <button
      type="submit"
      disabled={isSubmitting}
      className="w-full bg-cyan-600 text-white font-medium p-2 my-2 rounded-lg text-sm"
    >
      {isSubmitting ? "Submitting..." : "Submit"}
    </button>
  </form>
));

export default Post;
