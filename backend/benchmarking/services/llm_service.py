from openai import OpenAI
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.openrouter_client = OpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )

    def query_chatgpt(self, text):
        """
        Consulta ChatGPT (GPT-3.5-turbo) a través de OpenRouter.
        Ahora usa API_KEY y modelo desde settings.
        """
        try:
            response = self.openrouter_client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": text}
                ],
                max_tokens=2048
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error querying ChatGPT: {str(e)}")
            raise

    def query_deepseek(self, user_text):
        """
        Consulta DeepSeek a través de OpenRouter usando el prompt estructurado fijo.
        """
        prompt = (
            '''I need you to translate the information into structured natural 
            language and explain it to me in a paragraph in plain text format, 
            without literals, bullet points, or HTML. I'm 15 years old.\n\n'''
            f"{user_text}"
        )

        try:
            response = self.openrouter_client.chat.completions.create(
                model=settings.DEEPSEEK_MODEL,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2048
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error querying DeepSeek: {str(e)}")
            raise

    def process_with_llms(self, user_text):
        """
        Procesa el texto con ambos modelos y devuelve las respuestas.
        Por ahora ChatGPT devuelto como respuesta quemada de ejemplo.
        """
        chatgpt_res = '''This is a formal set of rules for a Tic-Tac-Toe game, 
        written in a programming style that defines the structure, actions, 
        and logic of the game. The board is a 3x3 grid where each cell can either be empty (denoted as "b"), 
        marked by player "x", or marked by player "o". The game starts with all cells empty, and player "x" goes first. 
        A player can only make a move by marking an empty cell. The game alternates between players, 
        and a player can mark a cell only if it's unoccupied. The game ends when one player creates 
        a line (horizontally, vertically, or diagonally) of three of their marks, or when all cells 
        are filled without any winner. The goal is to determine who won the game, or if it's a draw. If "x" wins, 
        the game assigns a score of 100 to "x" and 0 to "o". If both players have a line, they each score 50 points. 
        If there are no lines for either player, they also each score 50 points. The game checks for a terminal state whenever 
        a line is formed or when no more moves are possible. The rules also define the concept of a row, column, or diagonal 
        as a "line" of cells, which is essential to determining the winner.'''
        
        deepseek_res = self.query_deepseek(user_text)
        return chatgpt_res, deepseek_res
