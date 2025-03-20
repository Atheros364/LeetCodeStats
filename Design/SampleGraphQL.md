---Request---
{,…}
operationName
: 
"submissionList"
query
: 
"\n    query submissionList($offset: Int!, $limit: Int!, $lastKey: String, $questionSlug: String!, $lang: Int, $status: Int) {\n  questionSubmissionList(\n    offset: $offset\n    limit: $limit\n    lastKey: $lastKey\n    questionSlug: $questionSlug\n    lang: $lang\n    status: $status\n  ) {\n    lastKey\n    hasNext\n    submissions {\n      id\n      title\n      titleSlug\n      status\n      statusDisplay\n      lang\n      langName\n      runtime\n      timestamp\n      url\n      isPending\n      memory\n      hasNotes\n      notes\n      flagType\n      frontendId\n      topicTags {\n        id\n      }\n    }\n  }\n}\n    "
variables
: 
{questionSlug: "valid-palindrome-iii", offset: 0, limit: 20, lastKey: null}

---Response---
{
    "data": {
        "questionSubmissionList": {
            "lastKey": null,
            "hasNext": false,
            "submissions": [
                {
                    "id": "1579711140",
                    "title": "Valid Palindrome III",
                    "titleSlug": "valid-palindrome-iii",
                    "status": 10,
                    "statusDisplay": "Accepted",
                    "lang": "python3",
                    "langName": "Python3",
                    "runtime": "151 ms",
                    "timestamp": "1742438208",
                    "url": "/submissions/detail/1579711140/",
                    "isPending": "Not Pending",
                    "memory": "19.4 MB",
                    "hasNotes": false,
                    "notes": "",
                    "flagType": "WHITE",
                    "frontendId": 1,
                    "topicTags": []
                }
            ]
        }
    }
}


---Request---
{,…}
operationName
: 
"userProgressQuestionList"
query
: 
"\n    query userProgressQuestionList($filters: UserProgressQuestionListInput) {\n  userProgressQuestionList(filters: $filters) {\n    totalNum\n    questions {\n      translatedTitle\n      frontendId\n      title\n      titleSlug\n      difficulty\n      lastSubmittedAt\n      numSubmitted\n      questionStatus\n      lastResult\n      topicTags {\n        name\n        nameTranslated\n        slug\n      }\n    }\n  }\n}\n    "
variables
: 
{filters: {skip: 0, limit: 50}}
filters
: 
{skip: 0, limit: 50}

---Response---
{
    "data": {
        "userProgressQuestionList": {
            "totalNum": 340,
            "questions": [
                {
                    "translatedTitle": null,
                    "frontendId": "1216",
                    "title": "Valid Palindrome III",
                    "titleSlug": "valid-palindrome-iii",
                    "difficulty": "HARD",
                    "lastSubmittedAt": "2025-03-20T02:36:49+00:00",
                    "numSubmitted": 1,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "String",
                            "nameTranslated": "",
                            "slug": "string"
                        },
                        {
                            "name": "Dynamic Programming",
                            "nameTranslated": "",
                            "slug": "dynamic-programming"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "76",
                    "title": "Minimum Window Substring",
                    "titleSlug": "minimum-window-substring",
                    "difficulty": "HARD",
                    "lastSubmittedAt": "2025-03-20T02:06:31+00:00",
                    "numSubmitted": 10,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Hash Table",
                            "nameTranslated": "",
                            "slug": "hash-table"
                        },
                        {
                            "name": "String",
                            "nameTranslated": "",
                            "slug": "string"
                        },
                        {
                            "name": "Sliding Window",
                            "nameTranslated": "",
                            "slug": "sliding-window"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "239",
                    "title": "Sliding Window Maximum",
                    "titleSlug": "sliding-window-maximum",
                    "difficulty": "HARD",
                    "lastSubmittedAt": "2025-03-20T01:41:05+00:00",
                    "numSubmitted": 5,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Queue",
                            "nameTranslated": "",
                            "slug": "queue"
                        },
                        {
                            "name": "Sliding Window",
                            "nameTranslated": "",
                            "slug": "sliding-window"
                        },
                        {
                            "name": "Heap (Priority Queue)",
                            "nameTranslated": "",
                            "slug": "heap-priority-queue"
                        },
                        {
                            "name": "Monotonic Queue",
                            "nameTranslated": "",
                            "slug": "monotonic-queue"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "658",
                    "title": "Find K Closest Elements",
                    "titleSlug": "find-k-closest-elements",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-20T00:53:43+00:00",
                    "numSubmitted": 20,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Two Pointers",
                            "nameTranslated": "",
                            "slug": "two-pointers"
                        },
                        {
                            "name": "Binary Search",
                            "nameTranslated": "",
                            "slug": "binary-search"
                        },
                        {
                            "name": "Sliding Window",
                            "nameTranslated": "",
                            "slug": "sliding-window"
                        },
                        {
                            "name": "Sorting",
                            "nameTranslated": "",
                            "slug": "sorting"
                        },
                        {
                            "name": "Heap (Priority Queue)",
                            "nameTranslated": "",
                            "slug": "heap-priority-queue"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "209",
                    "title": "Minimum Size Subarray Sum",
                    "titleSlug": "minimum-size-subarray-sum",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-19T23:38:21+00:00",
                    "numSubmitted": 5,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Binary Search",
                            "nameTranslated": "",
                            "slug": "binary-search"
                        },
                        {
                            "name": "Sliding Window",
                            "nameTranslated": "",
                            "slug": "sliding-window"
                        },
                        {
                            "name": "Prefix Sum",
                            "nameTranslated": "",
                            "slug": "prefix-sum"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "567",
                    "title": "Permutation in String",
                    "titleSlug": "permutation-in-string",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-19T23:23:52+00:00",
                    "numSubmitted": 10,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Hash Table",
                            "nameTranslated": "",
                            "slug": "hash-table"
                        },
                        {
                            "name": "Two Pointers",
                            "nameTranslated": "",
                            "slug": "two-pointers"
                        },
                        {
                            "name": "String",
                            "nameTranslated": "",
                            "slug": "string"
                        },
                        {
                            "name": "Sliding Window",
                            "nameTranslated": "",
                            "slug": "sliding-window"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "424",
                    "title": "Longest Repeating Character Replacement",
                    "titleSlug": "longest-repeating-character-replacement",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-19T23:03:14+00:00",
                    "numSubmitted": 17,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Hash Table",
                            "nameTranslated": "",
                            "slug": "hash-table"
                        },
                        {
                            "name": "String",
                            "nameTranslated": "",
                            "slug": "string"
                        },
                        {
                            "name": "Sliding Window",
                            "nameTranslated": "",
                            "slug": "sliding-window"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "3",
                    "title": "Longest Substring Without Repeating Characters",
                    "titleSlug": "longest-substring-without-repeating-characters",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-19T22:32:02+00:00",
                    "numSubmitted": 34,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Hash Table",
                            "nameTranslated": "",
                            "slug": "hash-table"
                        },
                        {
                            "name": "String",
                            "nameTranslated": "",
                            "slug": "string"
                        },
                        {
                            "name": "Sliding Window",
                            "nameTranslated": "",
                            "slug": "sliding-window"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "121",
                    "title": "Best Time to Buy and Sell Stock",
                    "titleSlug": "best-time-to-buy-and-sell-stock",
                    "difficulty": "EASY",
                    "lastSubmittedAt": "2025-03-19T22:24:38+00:00",
                    "numSubmitted": 12,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Dynamic Programming",
                            "nameTranslated": "",
                            "slug": "dynamic-programming"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "219",
                    "title": "Contains Duplicate II",
                    "titleSlug": "contains-duplicate-ii",
                    "difficulty": "EASY",
                    "lastSubmittedAt": "2025-03-19T22:18:16+00:00",
                    "numSubmitted": 3,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Hash Table",
                            "nameTranslated": "",
                            "slug": "hash-table"
                        },
                        {
                            "name": "Sliding Window",
                            "nameTranslated": "",
                            "slug": "sliding-window"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "42",
                    "title": "Trapping Rain Water",
                    "titleSlug": "trapping-rain-water",
                    "difficulty": "HARD",
                    "lastSubmittedAt": "2025-03-19T04:45:14+00:00",
                    "numSubmitted": 3,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Two Pointers",
                            "nameTranslated": "",
                            "slug": "two-pointers"
                        },
                        {
                            "name": "Dynamic Programming",
                            "nameTranslated": "",
                            "slug": "dynamic-programming"
                        },
                        {
                            "name": "Stack",
                            "nameTranslated": "",
                            "slug": "stack"
                        },
                        {
                            "name": "Monotonic Stack",
                            "nameTranslated": "",
                            "slug": "monotonic-stack"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "881",
                    "title": "Boats to Save People",
                    "titleSlug": "boats-to-save-people",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-19T04:36:41+00:00",
                    "numSubmitted": 1,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Two Pointers",
                            "nameTranslated": "",
                            "slug": "two-pointers"
                        },
                        {
                            "name": "Greedy",
                            "nameTranslated": "",
                            "slug": "greedy"
                        },
                        {
                            "name": "Sorting",
                            "nameTranslated": "",
                            "slug": "sorting"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "11",
                    "title": "Container With Most Water",
                    "titleSlug": "container-with-most-water",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-19T04:31:16+00:00",
                    "numSubmitted": 6,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Two Pointers",
                            "nameTranslated": "",
                            "slug": "two-pointers"
                        },
                        {
                            "name": "Greedy",
                            "nameTranslated": "",
                            "slug": "greedy"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "18",
                    "title": "4Sum",
                    "titleSlug": "4sum",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-19T04:27:44+00:00",
                    "numSubmitted": 8,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Two Pointers",
                            "nameTranslated": "",
                            "slug": "two-pointers"
                        },
                        {
                            "name": "Sorting",
                            "nameTranslated": "",
                            "slug": "sorting"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "189",
                    "title": "Rotate Array",
                    "titleSlug": "rotate-array",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-17T23:55:12+00:00",
                    "numSubmitted": 11,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Math",
                            "nameTranslated": "",
                            "slug": "math"
                        },
                        {
                            "name": "Two Pointers",
                            "nameTranslated": "",
                            "slug": "two-pointers"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "15",
                    "title": "3Sum",
                    "titleSlug": "3sum",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-17T23:26:15+00:00",
                    "numSubmitted": 38,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Two Pointers",
                            "nameTranslated": "",
                            "slug": "two-pointers"
                        },
                        {
                            "name": "Sorting",
                            "nameTranslated": "",
                            "slug": "sorting"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "167",
                    "title": "Two Sum II - Input Array Is Sorted",
                    "titleSlug": "two-sum-ii-input-array-is-sorted",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-17T22:58:52+00:00",
                    "numSubmitted": 9,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Two Pointers",
                            "nameTranslated": "",
                            "slug": "two-pointers"
                        },
                        {
                            "name": "Binary Search",
                            "nameTranslated": "",
                            "slug": "binary-search"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "26",
                    "title": "Remove Duplicates from Sorted Array",
                    "titleSlug": "remove-duplicates-from-sorted-array",
                    "difficulty": "EASY",
                    "lastSubmittedAt": "2025-03-17T22:28:59+00:00",
                    "numSubmitted": 7,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Two Pointers",
                            "nameTranslated": "",
                            "slug": "two-pointers"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "88",
                    "title": "Merge Sorted Array",
                    "titleSlug": "merge-sorted-array",
                    "difficulty": "EASY",
                    "lastSubmittedAt": "2025-03-17T22:26:41+00:00",
                    "numSubmitted": 15,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Two Pointers",
                            "nameTranslated": "",
                            "slug": "two-pointers"
                        },
                        {
                            "name": "Sorting",
                            "nameTranslated": "",
                            "slug": "sorting"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "1768",
                    "title": "Merge Strings Alternately",
                    "titleSlug": "merge-strings-alternately",
                    "difficulty": "EASY",
                    "lastSubmittedAt": "2025-03-17T22:17:49+00:00",
                    "numSubmitted": 5,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Two Pointers",
                            "nameTranslated": "",
                            "slug": "two-pointers"
                        },
                        {
                            "name": "String",
                            "nameTranslated": "",
                            "slug": "string"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "680",
                    "title": "Valid Palindrome II",
                    "titleSlug": "valid-palindrome-ii",
                    "difficulty": "EASY",
                    "lastSubmittedAt": "2025-03-17T22:13:39+00:00",
                    "numSubmitted": 11,
                    "questionStatus": "SOLVED",
                    "lastResult": "WA",
                    "topicTags": [
                        {
                            "name": "Two Pointers",
                            "nameTranslated": "",
                            "slug": "two-pointers"
                        },
                        {
                            "name": "String",
                            "nameTranslated": "",
                            "slug": "string"
                        },
                        {
                            "name": "Greedy",
                            "nameTranslated": "",
                            "slug": "greedy"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "344",
                    "title": "Reverse String",
                    "titleSlug": "reverse-string",
                    "difficulty": "EASY",
                    "lastSubmittedAt": "2025-03-17T22:05:27+00:00",
                    "numSubmitted": 5,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Two Pointers",
                            "nameTranslated": "",
                            "slug": "two-pointers"
                        },
                        {
                            "name": "String",
                            "nameTranslated": "",
                            "slug": "string"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "125",
                    "title": "Valid Palindrome",
                    "titleSlug": "valid-palindrome",
                    "difficulty": "EASY",
                    "lastSubmittedAt": "2025-03-17T22:02:42+00:00",
                    "numSubmitted": 10,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Two Pointers",
                            "nameTranslated": "",
                            "slug": "two-pointers"
                        },
                        {
                            "name": "String",
                            "nameTranslated": "",
                            "slug": "string"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "41",
                    "title": "First Missing Positive",
                    "titleSlug": "first-missing-positive",
                    "difficulty": "HARD",
                    "lastSubmittedAt": "2025-03-17T05:56:18+00:00",
                    "numSubmitted": 9,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Hash Table",
                            "nameTranslated": "",
                            "slug": "hash-table"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "560",
                    "title": "Subarray Sum Equals K",
                    "titleSlug": "subarray-sum-equals-k",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-17T05:25:09+00:00",
                    "numSubmitted": 12,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Hash Table",
                            "nameTranslated": "",
                            "slug": "hash-table"
                        },
                        {
                            "name": "Prefix Sum",
                            "nameTranslated": "",
                            "slug": "prefix-sum"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "229",
                    "title": "Majority Element II",
                    "titleSlug": "majority-element-ii",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-17T05:11:52+00:00",
                    "numSubmitted": 3,
                    "questionStatus": "SOLVED",
                    "lastResult": "WA",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Hash Table",
                            "nameTranslated": "",
                            "slug": "hash-table"
                        },
                        {
                            "name": "Sorting",
                            "nameTranslated": "",
                            "slug": "sorting"
                        },
                        {
                            "name": "Counting",
                            "nameTranslated": "",
                            "slug": "counting"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "122",
                    "title": "Best Time to Buy and Sell Stock II",
                    "titleSlug": "best-time-to-buy-and-sell-stock-ii",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-17T04:51:03+00:00",
                    "numSubmitted": 6,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Dynamic Programming",
                            "nameTranslated": "",
                            "slug": "dynamic-programming"
                        },
                        {
                            "name": "Greedy",
                            "nameTranslated": "",
                            "slug": "greedy"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "128",
                    "title": "Longest Consecutive Sequence",
                    "titleSlug": "longest-consecutive-sequence",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-17T04:47:18+00:00",
                    "numSubmitted": 12,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Hash Table",
                            "nameTranslated": "",
                            "slug": "hash-table"
                        },
                        {
                            "name": "Union Find",
                            "nameTranslated": "",
                            "slug": "union-find"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "36",
                    "title": "Valid Sudoku",
                    "titleSlug": "valid-sudoku",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-17T04:18:27+00:00",
                    "numSubmitted": 12,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Hash Table",
                            "nameTranslated": "",
                            "slug": "hash-table"
                        },
                        {
                            "name": "Matrix",
                            "nameTranslated": "",
                            "slug": "matrix"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "238",
                    "title": "Product of Array Except Self",
                    "titleSlug": "product-of-array-except-self",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-17T04:06:22+00:00",
                    "numSubmitted": 7,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Prefix Sum",
                            "nameTranslated": "",
                            "slug": "prefix-sum"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "304",
                    "title": "Range Sum Query 2D - Immutable",
                    "titleSlug": "range-sum-query-2d-immutable",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-17T03:55:23+00:00",
                    "numSubmitted": 4,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Design",
                            "nameTranslated": "",
                            "slug": "design"
                        },
                        {
                            "name": "Matrix",
                            "nameTranslated": "",
                            "slug": "matrix"
                        },
                        {
                            "name": "Prefix Sum",
                            "nameTranslated": "",
                            "slug": "prefix-sum"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "271",
                    "title": "Encode and Decode Strings",
                    "titleSlug": "encode-and-decode-strings",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-17T03:34:22+00:00",
                    "numSubmitted": 8,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "String",
                            "nameTranslated": "",
                            "slug": "string"
                        },
                        {
                            "name": "Design",
                            "nameTranslated": "",
                            "slug": "design"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "347",
                    "title": "Top K Frequent Elements",
                    "titleSlug": "top-k-frequent-elements",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-17T03:26:08+00:00",
                    "numSubmitted": 6,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Hash Table",
                            "nameTranslated": "",
                            "slug": "hash-table"
                        },
                        {
                            "name": "Divide and Conquer",
                            "nameTranslated": "",
                            "slug": "divide-and-conquer"
                        },
                        {
                            "name": "Sorting",
                            "nameTranslated": "",
                            "slug": "sorting"
                        },
                        {
                            "name": "Heap (Priority Queue)",
                            "nameTranslated": "",
                            "slug": "heap-priority-queue"
                        },
                        {
                            "name": "Bucket Sort",
                            "nameTranslated": "",
                            "slug": "bucket-sort"
                        },
                        {
                            "name": "Counting",
                            "nameTranslated": "",
                            "slug": "counting"
                        },
                        {
                            "name": "Quickselect",
                            "nameTranslated": "",
                            "slug": "quickselect"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "75",
                    "title": "Sort Colors",
                    "titleSlug": "sort-colors",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-17T02:25:11+00:00",
                    "numSubmitted": 8,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Two Pointers",
                            "nameTranslated": "",
                            "slug": "two-pointers"
                        },
                        {
                            "name": "Sorting",
                            "nameTranslated": "",
                            "slug": "sorting"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "912",
                    "title": "Sort an Array",
                    "titleSlug": "sort-an-array",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-17T02:11:43+00:00",
                    "numSubmitted": 2,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Divide and Conquer",
                            "nameTranslated": "",
                            "slug": "divide-and-conquer"
                        },
                        {
                            "name": "Sorting",
                            "nameTranslated": "",
                            "slug": "sorting"
                        },
                        {
                            "name": "Heap (Priority Queue)",
                            "nameTranslated": "",
                            "slug": "heap-priority-queue"
                        },
                        {
                            "name": "Merge Sort",
                            "nameTranslated": "",
                            "slug": "merge-sort"
                        },
                        {
                            "name": "Bucket Sort",
                            "nameTranslated": "",
                            "slug": "bucket-sort"
                        },
                        {
                            "name": "Radix Sort",
                            "nameTranslated": "",
                            "slug": "radix-sort"
                        },
                        {
                            "name": "Counting Sort",
                            "nameTranslated": "",
                            "slug": "counting-sort"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "706",
                    "title": "Design HashMap",
                    "titleSlug": "design-hashmap",
                    "difficulty": "EASY",
                    "lastSubmittedAt": "2025-03-17T01:16:15+00:00",
                    "numSubmitted": 1,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Hash Table",
                            "nameTranslated": "",
                            "slug": "hash-table"
                        },
                        {
                            "name": "Linked List",
                            "nameTranslated": "",
                            "slug": "linked-list"
                        },
                        {
                            "name": "Design",
                            "nameTranslated": "",
                            "slug": "design"
                        },
                        {
                            "name": "Hash Function",
                            "nameTranslated": "",
                            "slug": "hash-function"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "705",
                    "title": "Design HashSet",
                    "titleSlug": "design-hashset",
                    "difficulty": "EASY",
                    "lastSubmittedAt": "2025-03-17T01:08:12+00:00",
                    "numSubmitted": 2,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Hash Table",
                            "nameTranslated": "",
                            "slug": "hash-table"
                        },
                        {
                            "name": "Linked List",
                            "nameTranslated": "",
                            "slug": "linked-list"
                        },
                        {
                            "name": "Design",
                            "nameTranslated": "",
                            "slug": "design"
                        },
                        {
                            "name": "Hash Function",
                            "nameTranslated": "",
                            "slug": "hash-function"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "169",
                    "title": "Majority Element",
                    "titleSlug": "majority-element",
                    "difficulty": "EASY",
                    "lastSubmittedAt": "2025-03-17T01:04:29+00:00",
                    "numSubmitted": 4,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Hash Table",
                            "nameTranslated": "",
                            "slug": "hash-table"
                        },
                        {
                            "name": "Divide and Conquer",
                            "nameTranslated": "",
                            "slug": "divide-and-conquer"
                        },
                        {
                            "name": "Sorting",
                            "nameTranslated": "",
                            "slug": "sorting"
                        },
                        {
                            "name": "Counting",
                            "nameTranslated": "",
                            "slug": "counting"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "27",
                    "title": "Remove Element",
                    "titleSlug": "remove-element",
                    "difficulty": "EASY",
                    "lastSubmittedAt": "2025-03-17T01:01:22+00:00",
                    "numSubmitted": 5,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Two Pointers",
                            "nameTranslated": "",
                            "slug": "two-pointers"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "49",
                    "title": "Group Anagrams",
                    "titleSlug": "group-anagrams",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-16T23:51:19+00:00",
                    "numSubmitted": 13,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Hash Table",
                            "nameTranslated": "",
                            "slug": "hash-table"
                        },
                        {
                            "name": "String",
                            "nameTranslated": "",
                            "slug": "string"
                        },
                        {
                            "name": "Sorting",
                            "nameTranslated": "",
                            "slug": "sorting"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "14",
                    "title": "Longest Common Prefix",
                    "titleSlug": "longest-common-prefix",
                    "difficulty": "EASY",
                    "lastSubmittedAt": "2025-03-16T23:45:06+00:00",
                    "numSubmitted": 15,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "String",
                            "nameTranslated": "",
                            "slug": "string"
                        },
                        {
                            "name": "Trie",
                            "nameTranslated": "",
                            "slug": "trie"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "1",
                    "title": "Two Sum",
                    "titleSlug": "two-sum",
                    "difficulty": "EASY",
                    "lastSubmittedAt": "2025-03-16T23:33:36+00:00",
                    "numSubmitted": 17,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Hash Table",
                            "nameTranslated": "",
                            "slug": "hash-table"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "242",
                    "title": "Valid Anagram",
                    "titleSlug": "valid-anagram",
                    "difficulty": "EASY",
                    "lastSubmittedAt": "2025-03-16T23:32:20+00:00",
                    "numSubmitted": 3,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Hash Table",
                            "nameTranslated": "",
                            "slug": "hash-table"
                        },
                        {
                            "name": "String",
                            "nameTranslated": "",
                            "slug": "string"
                        },
                        {
                            "name": "Sorting",
                            "nameTranslated": "",
                            "slug": "sorting"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "217",
                    "title": "Contains Duplicate",
                    "titleSlug": "contains-duplicate",
                    "difficulty": "EASY",
                    "lastSubmittedAt": "2025-03-16T23:31:39+00:00",
                    "numSubmitted": 5,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Hash Table",
                            "nameTranslated": "",
                            "slug": "hash-table"
                        },
                        {
                            "name": "Sorting",
                            "nameTranslated": "",
                            "slug": "sorting"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "1929",
                    "title": "Concatenation of Array",
                    "titleSlug": "concatenation-of-array",
                    "difficulty": "EASY",
                    "lastSubmittedAt": "2025-03-16T23:30:28+00:00",
                    "numSubmitted": 2,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Simulation",
                            "nameTranslated": "",
                            "slug": "simulation"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "1489",
                    "title": "Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree",
                    "titleSlug": "find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree",
                    "difficulty": "HARD",
                    "lastSubmittedAt": "2025-03-16T21:41:35+00:00",
                    "numSubmitted": 2,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Union Find",
                            "nameTranslated": "",
                            "slug": "union-find"
                        },
                        {
                            "name": "Graph",
                            "nameTranslated": "",
                            "slug": "graph"
                        },
                        {
                            "name": "Sorting",
                            "nameTranslated": "",
                            "slug": "sorting"
                        },
                        {
                            "name": "Minimum Spanning Tree",
                            "nameTranslated": "",
                            "slug": "minimum-spanning-tree"
                        },
                        {
                            "name": "Strongly Connected Component",
                            "nameTranslated": "",
                            "slug": "strongly-connected-component"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "269",
                    "title": "Alien Dictionary",
                    "titleSlug": "alien-dictionary",
                    "difficulty": "HARD",
                    "lastSubmittedAt": "2025-03-16T05:38:52+00:00",
                    "numSubmitted": 12,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "String",
                            "nameTranslated": "",
                            "slug": "string"
                        },
                        {
                            "name": "Depth-First Search",
                            "nameTranslated": "",
                            "slug": "depth-first-search"
                        },
                        {
                            "name": "Breadth-First Search",
                            "nameTranslated": "",
                            "slug": "breadth-first-search"
                        },
                        {
                            "name": "Graph",
                            "nameTranslated": "",
                            "slug": "graph"
                        },
                        {
                            "name": "Topological Sort",
                            "nameTranslated": "",
                            "slug": "topological-sort"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "778",
                    "title": "Swim in Rising Water",
                    "titleSlug": "swim-in-rising-water",
                    "difficulty": "HARD",
                    "lastSubmittedAt": "2025-03-16T04:57:20+00:00",
                    "numSubmitted": 5,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Binary Search",
                            "nameTranslated": "",
                            "slug": "binary-search"
                        },
                        {
                            "name": "Depth-First Search",
                            "nameTranslated": "",
                            "slug": "depth-first-search"
                        },
                        {
                            "name": "Breadth-First Search",
                            "nameTranslated": "",
                            "slug": "breadth-first-search"
                        },
                        {
                            "name": "Union Find",
                            "nameTranslated": "",
                            "slug": "union-find"
                        },
                        {
                            "name": "Heap (Priority Queue)",
                            "nameTranslated": "",
                            "slug": "heap-priority-queue"
                        },
                        {
                            "name": "Matrix",
                            "nameTranslated": "",
                            "slug": "matrix"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "332",
                    "title": "Reconstruct Itinerary",
                    "titleSlug": "reconstruct-itinerary",
                    "difficulty": "HARD",
                    "lastSubmittedAt": "2025-03-16T00:26:35+00:00",
                    "numSubmitted": 4,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Depth-First Search",
                            "nameTranslated": "",
                            "slug": "depth-first-search"
                        },
                        {
                            "name": "Graph",
                            "nameTranslated": "",
                            "slug": "graph"
                        },
                        {
                            "name": "Eulerian Circuit",
                            "nameTranslated": "",
                            "slug": "eulerian-circuit"
                        }
                    ]
                },
                {
                    "translatedTitle": null,
                    "frontendId": "139",
                    "title": "Word Break",
                    "titleSlug": "word-break",
                    "difficulty": "MEDIUM",
                    "lastSubmittedAt": "2025-03-15T21:19:32+00:00",
                    "numSubmitted": 8,
                    "questionStatus": "SOLVED",
                    "lastResult": "AC",
                    "topicTags": [
                        {
                            "name": "Array",
                            "nameTranslated": "",
                            "slug": "array"
                        },
                        {
                            "name": "Hash Table",
                            "nameTranslated": "",
                            "slug": "hash-table"
                        },
                        {
                            "name": "String",
                            "nameTranslated": "",
                            "slug": "string"
                        },
                        {
                            "name": "Dynamic Programming",
                            "nameTranslated": "",
                            "slug": "dynamic-programming"
                        },
                        {
                            "name": "Trie",
                            "nameTranslated": "",
                            "slug": "trie"
                        },
                        {
                            "name": "Memoization",
                            "nameTranslated": "",
                            "slug": "memoization"
                        }
                    ]
                }
            ]
        }
    }
}