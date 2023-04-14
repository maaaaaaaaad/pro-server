import { PickType } from '@nestjs/swagger'
import { CommentEntity } from '../entities/comment.entity'

export class CommentRegisterInputDto extends PickType(CommentEntity, [
  'content',
  'itemId',
]) {}
