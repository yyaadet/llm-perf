import pandas as pd
import json
from pathlib import Path


class PromptGenerate:

    def __init__(self, work_dir, output) -> None:
        self.work_dir = Path(work_dir)
        self.output = Path(output)
        self.subjects: dict = {} 
        with open(str(self.work_dir / "subject_mapping.json")) as f:
            self.subjects = json.load(f)
        self.category_count_map = dict()

    def generate(self):
        output_f = open(self.output, "w")
        for subject, names in self.subjects.items():
            zh_subject = names[1]
            category = names[2]
            val_path = self.work_dir / "val" / f"{subject}_val.csv"
            val_df = pd.read_csv(val_path)
            for idx, row in val_df.iterrows():
                prompt = self.get_template(zh_subject, row['question'], row['A'], row['B'], row['C'], row['D'])
                answer = row['answer']
                output_f.write(json.dumps({'prompt': prompt, 'answer': answer, 'category': category, 'subject': zh_subject}, ensure_ascii=False))
                output_f.write("\n")
                if category in self.category_count_map:
                    self.category_count_map[category] += 1
                else:
                    self.category_count_map[category] = 1

        output_f.close()

        for category, count in self.category_count_map.items():
            print(f"{category}: {count}")
    
    def get_template(self, zh_subject, question, a, b, c, d):
        prompt = f"以下是中国关于{zh_subject}考试的单项选择题，请选出其中的正确答案。\n"
        prompt += f"{question}\n"
        prompt += f"A. {a}\n"
        prompt += f"B. {b}\n"
        prompt += f"C. {c}\n"
        prompt += f"D. {d}\n"
        
        return prompt
        


if __name__ == '__main__':
    generator = PromptGenerate(".", "ceval.json")
    generator.generate()
