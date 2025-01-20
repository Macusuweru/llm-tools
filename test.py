tags = {
    "tag1": {"tag1.1": ["tag1.1.1", "tag1.1.2"],
             "tag1.2": ["tag1.2.1"]},
    "tag2": {"tag2.1": ["tag2.1.1"]}
}
for tag in tags:
    print(tag == "tag1")