"""Fixes issue with dist build where the frontend files are not found due to subdirectory path issues."""

# read file from frontend/dist/index.html


def fix_dist(app_dir="/app"):
    """Fixes issue with dist build where the frontend files are not found due to subdirectory path issues."""
    with open("./frontend/dist/index.html", "r", encoding="utf-8") as file:

        link_sources = ["href=", "src="]

        # save the new lines to write back to the file
        new_lines = []

        for line in file:

            # by default keep line as is
            new_line = line

            for link_source in link_sources:

                # don't add if already added
                if app_dir in line:
                    continue

                if link_source in line:
                    # start is the end of the link source eg. href="! or src="!
                    # where ! is the position where the subdirectory should be inserted
                    insert_index = line.find(link_source) + len(link_source) + 1

                    # we need to add app_dir to the link
                    new_line = line[:insert_index] + app_dir + line[insert_index:]

            # append new line
            new_lines.append(new_line)

    # write new file
    with open("./frontend/dist/index.html", "w", encoding="utf-8") as file:
        file.writelines(new_lines)


if __name__ == "__main__":
    fix_dist()
