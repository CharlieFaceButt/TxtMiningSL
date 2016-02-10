package edu.lsc.smm;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.FilenameFilter;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.StringTokenizer;

import com.restfb.Connection;
import com.restfb.DefaultFacebookClient;
import com.restfb.FacebookClient;
import com.restfb.Parameter;
import com.restfb.Version;
import com.restfb.json.JsonArray;
import com.restfb.json.JsonObject;
import com.restfb.types.Comment;
import com.restfb.types.Page;
import com.restfb.types.Post;

public class Miner {

	public static String accessToken;
	private static final int MaxCommentCountPerPost = 10;
	
	/**
	 * Authorized Facebook connection client
	 * @return
	 */
	private static FacebookClient getAuthClient(){
		//OAuth
		Miner.accessToken = "CAACEdEose0cBAOO8AspKmsp5F38xuZB7RnuAWJv6rtkCc1aM9jHBbd0y5MPZCDBRYWWZAaEXTfffG6UZAqMMF8pZCABXVLJ4fr66hrlLAfXV4BXIZBtWZA6V3ZCMBfVr7uBiag2lNlHrKA2FUNQo5mj8UHIrDCI9IVVZC5P06fTNh3YCDa38t7ZCwh9kfIWkf9i3ySjoZA6QzXDXQZDZD";
		FacebookClient client = new DefaultFacebookClient(
				Miner.accessToken, Version.VERSION_2_5);
		return client;
	}
	
	/**
	 * Get comments of a post using facebook Graph API
	 * @param client
	 * @param post
	 * @return comments in JSON array
	 */
	private static JsonArray getComments(FacebookClient client, Post post){
		JsonArray ja = new JsonArray();
		Connection<Comment> comment_result = client.fetchConnection(post.getId() + "/comments", Comment.class);
		List<Comment> comments = comment_result.getData();
		for (int i = 0; i < comments.size() && i < MaxCommentCountPerPost; i++) {
			JsonObject jo = new JsonObject();
			Comment cmt = comments.get(i);
			jo.put("id", cmt.getId());
			jo.put("message", cmt.getMessage());
			jo.put("createdTime", cmt.getCreatedTime());
			ja.put(jo);
		}
		return ja;
	}
	
	/**
	 * Get data using facebook Graph API
	 * @param topic
	 */
	public static void retriveData(String topic){
		if (topic == null || topic.length() == 0) {
			topic = "Virtual Reality";
		}
		
		//Authorization
		FacebookClient client = getAuthClient();

		//Amount of pages
		int pageCount = 0;
		//Total amount of posts
		int totalPostCount = 0;
		
		//Output data
		JsonArray resultArray = new JsonArray();

		//Search for page by topic
		Connection<Page> targetedSearch = client.fetchConnection(
				"search", 
				Page.class, 
				Parameter.with("q", topic), 
				Parameter.with("type", "page"));
		
		//Traverse all result pages to get enough data files
		String nextDataUrl = null;
		int fileNumber = 0;
		while(fileNumber < 10){ 		//At most 10 files
			
			//Need to visit next page
			if (targetedSearch == null) {
				
				//Entire result data in current collection is visited
				if (nextDataUrl == null) {
					System.out.println("end of search result");
					break;
				}
				
				//Refresh output data
				resultArray = new JsonArray();
				
				//Get next collection of data
				targetedSearch = client.fetchConnectionPage(nextDataUrl, Page.class);
			}
			
			
			//Get posts
			
			List<Page> list = targetedSearch.getData();
			for (int i = 0; i < list.size(); i++) {
				//Get page
				JsonObject fbpage = client.fetchObject(list.get(i).getId(), JsonObject.class);
				pageCount ++;
				
				//Get related posts
				Connection<Post> relatedPosts = client.fetchConnection(
						list.get(i).getId() + "/posts", Post.class); 
				List<Post> posts = relatedPosts.getData();
				
				//Add posts into output data
				int N = posts.size();
				totalPostCount += N;
				System.out.println("Page" + pageCount + ":" + list.get(i).getName() + ";\t related post:" + N);
				
				//Traverse at most 25 posts
				for (int j = 0; j < N; j++) {
					
					JsonArray ja;
					try {
						ja = fbpage.getJsonArray("posts");
					} catch (Exception e) {
						// TODO Auto-generated catch block
	//					e.printStackTrace();
						ja = new JsonArray();
					}
					
					//Add post into output data
					JsonObject post = new JsonObject();
					Post pagePost = posts.get(j);
					post.put("id", pagePost.getId());
					post.put("message", pagePost.getMessage());
					post.put("createdTime", pagePost.getCreatedTime());
					post.put("comments", getComments(client, pagePost));
					ja.put(post);
					fbpage.put("posts", ja);
				}
				resultArray.put(fbpage);
			}

			//Next page of data
			nextDataUrl = targetedSearch.getNextPageUrl();
			targetedSearch = null;
			if (totalPostCount >= 500) {
				fileNumber ++;
				//save to file
				try {
					writeJsonArrayToFile(resultArray, "./data/openSource" + fileNumber + ".json");
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
					break;
				}
				System.out.println("Post count in this file: " + totalPostCount);
				totalPostCount += totalPostCount;
				totalPostCount = 0;
			}
			
		}
	}
	
	public static void main(String[] args) {
//		Miner.retriveData("Open Source");
		System.out.println(Miner.basicStatistisOfData());
	}
	
	
	private static void writeJsonArrayToFile(JsonArray array, String filename) throws IOException{
		try (FileWriter file = new FileWriter(filename)) {
			file.write(array.toString(4));
			System.out.println("Successfully Copied JSON Object to File: " + filename);
		}
	}
	
	public static JsonObject basicStatistisOfData(){

		//Total amount of pages
		int totalPageCount = 0;
		//Total amount of posts
		int totalPostCount = 0;
		//Total amount of comments
		int totalCommentCount = 0;
		//Total amount of words in collection of posts
		int totalPostWords = 0;
		//Total amount of words in collection of comments
		int totalCommentWords = 0;
		
		//Open data files
		File dir = new File("./data");
		File[] fileList = dir.listFiles(new FilenameFilter() {
			@Override
			public boolean accept(File dir, String name) {
				// TODO Auto-generated method stub
				if (name.contains("openSource")) {
					return true;
				}
				return false;
			}
		});
		
		//Tokenizer
		StringTokenizer tokenizer = null;
		//Post word map
		Map<String, Integer> postMap = new HashMap<String, Integer>();
		//Comment word map
		Map<String, Integer> commentMap = new HashMap<String, Integer>();
		
		//Traverse all file data
		for (File file: fileList){
			
			//Get all facebook page data
			JsonArray pages = new JsonArray(getStringFromFile(file));
			int PGN = pages.length();
			totalPageCount += PGN;
			
			//For each page
			for (int i = 0; i < PGN; i++) {
				JsonObject page = pages.getJsonObject(i);
				
				//Get posts of page
				JsonArray posts;
				try {
					posts = page.getJsonArray("posts");
				} catch (Exception e1) {
					System.err.println("NULL post in page");
					continue;
				}
				int PTN = posts.length();
				totalPostCount += PTN;
				
				//For each post
				for (int j = 0; j < PTN; j++) {
					JsonObject post = posts.getJsonObject(j);
					String postMsg;
					try {
						postMsg = (String)post.get("message");
					} catch (Exception e) {
//						e.printStackTrace();
						System.err.println("NULL msg in post");
						continue;
					}
					
					//Tokenize post message
					tokenizer = new StringTokenizer(postMsg);
					while (tokenizer.hasMoreElements()) {
						String postWord = (String) tokenizer.nextElement();
						Integer pwc = postMap.get(postWord);
						if (pwc == null) {
							pwc = 0;
						}
						postMap.put(postWord, pwc + 1);
						totalPostWords ++;
					}
					
					//Get comment of post
					JsonArray comments;
					try {
						comments = post.getJsonArray("comments");
					} catch (Exception e1) {
						System.err.println("NULL comment in post");
						continue;
					}
					int CMN = comments.length();
					totalCommentCount += CMN;
					
					//For each comment
					for (int k = 0; k < CMN; k++) {
						JsonObject comment = comments.getJsonObject(k);
						String cmtMsg;
						try {
							cmtMsg = comment.getString("message");
						} catch (Exception e) {
							System.err.println("NULL msg in comment");
							continue;
						}
						
						//Tokenize comment message
						tokenizer = new StringTokenizer(cmtMsg);
						while (tokenizer.hasMoreElements()) {
							String commentWord = (String) tokenizer.nextElement();
							Integer cwc = commentMap.get(commentWord);
							if (cwc == null) {
								cwc = 0;
							}
							commentMap.put(commentWord, cwc + 1);
							totalCommentWords ++;
						}
					}//end of comment traverse
				}//end of post traverse
			}//end of page traverse
		}//end of file traverse
		
		
		
		JsonObject stat = new JsonObject();
		stat.put("page#", totalPageCount);
		stat.put("post#", totalPostCount);
		stat.put("comment#", totalCommentCount);
		stat.put("average number of words per post", (double)totalPostWords / totalPostCount);
		stat.put("average number of words per comment", (double)totalCommentWords / totalCommentCount);
		stat.put("lexical diversity of posts", (double)(postMap.size()) / totalPostWords);
		stat.put("lexical diversity of comments", (double)(commentMap.size()) / totalCommentWords);
		return stat;
	}
	
	private static String getStringFromFile(File file){
		System.out.println("file: " + file);
	    String result = "";
	    try {
	        BufferedReader br = new BufferedReader(new FileReader(file));
	        StringBuilder sb = new StringBuilder();
	        String line = br.readLine();
	        while (line != null) {
	            sb.append(line);
	            line = br.readLine();
	        }
	        result = sb.toString();
	    } catch(Exception e) {
	        e.printStackTrace();
	    }
	    return result;
	}
}
